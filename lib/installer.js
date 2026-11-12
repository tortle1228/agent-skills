import fs from 'node:fs/promises';
import path from 'node:path';
import { createHash } from 'node:crypto';

const owner = 'agent-skills';
const marker = '.agent-skills-install.json';

export async function listSkills(root) {
  const skills = [];
  for (const entry of (await fs.readdir(path.join(root, 'skills'), { withFileTypes: true })).sort((a, b) => a.name.localeCompare(b.name))) {
    if (entry.isDirectory() && await exists(path.join(root, 'skills', entry.name, 'SKILL.md'))) skills.push(entry.name);
  }
  return skills;
}

export function targetFor(home, agent, skill) {
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(skill ?? '')) throw new Error(`Invalid skill name: ${skill}`);
  if (agent === 'codex') return path.join(home, '.agents', 'skills', skill);
  if (agent === 'claude-code') return path.join(home, '.claude', 'skills', skill);
  throw new Error(`Unknown agent: ${agent}`);
}

async function exists(file) {
  try { return await fs.lstat(file); }
  catch (error) { if (error.code === 'ENOENT') return null; throw error; }
}

async function hashes(directory, skipMarker, prefix = '') {
  const result = {};
  for (const entry of (await fs.readdir(path.join(directory, prefix))).sort()) {
    if (!prefix && entry === skipMarker) continue;
    const relative = prefix ? `${prefix}/${entry}` : entry;
    const file = path.join(directory, relative);
    const stat = await fs.lstat(file);
    if (stat.isSymbolicLink()) throw new Error(`Refusing symbolic link: ${file}`);
    if (stat.isDirectory()) Object.assign(result, await hashes(directory, skipMarker, relative));
    else if (stat.isFile()) result[relative] = createHash('sha256').update(await fs.readFile(file)).digest('hex');
    else throw new Error(`Unsupported file: ${file}`);
  }
  return result;
}

function validRecord(state, record) {
  if (state.owner !== record.owner || state.schema !== 1 || typeof state.version !== 'string' || !state.files || typeof state.files !== 'object') return false;
  return state.skill === record.skill;
}

async function managedState(target, record) {
  const stat = await exists(target);
  if (!stat) return null;
  if (stat.isSymbolicLink() || !stat.isDirectory()) throw new Error(`Refusing existing non-directory or symlink: ${target}`);
  let state;
  try {
    const markerStat = await fs.lstat(path.join(target, record.marker));
    if (!markerStat.isFile() || markerStat.isSymbolicLink()) throw new Error('Invalid marker');
    state = JSON.parse(await fs.readFile(path.join(target, record.marker), 'utf8'));
  } catch { throw new Error(`Unmanaged installation; leave it untouched: ${target}`); }
  if (!validRecord(state, record)) throw new Error(`Unrecognized installation record: ${target}`);
  const current = await hashes(target, record.marker);
  const keys = Object.keys(current);
  if (keys.length !== Object.keys(state.files).length || keys.some(key => current[key] !== state.files[key])) {
    throw new Error(`Locally modified installation; preserve or remove your changes before retrying: ${target}`);
  }
  return state;
}

const recordFor = skill => ({ owner, marker, skill });

export async function install(root, skill, target, version) {
  const source = path.join(root, 'skills', skill);
  if (!await exists(path.join(source, 'SKILL.md'))) throw new Error(`Unknown skill: ${skill}`);
  const previous = await managedState(target, recordFor(skill));
  await fs.mkdir(path.dirname(target), { recursive: true });
  const staging = await fs.mkdtemp(path.join(path.dirname(target), `.${owner}-`));
  const incoming = path.join(staging, 'incoming');
  const backup = path.join(staging, 'previous');
  let preserveBackup = false;
  try {
    await fs.cp(source, incoming, { recursive: true, dereference: false });
    if (!await exists(path.join(incoming, 'LICENSE'))) await fs.copyFile(path.join(root, 'LICENSE'), path.join(incoming, 'LICENSE'));
    const files = await hashes(incoming, marker);
    if (previous?.version === version && JSON.stringify(previous.files) === JSON.stringify(files)) return 'Already installed';
    await fs.writeFile(path.join(incoming, marker), JSON.stringify({ owner, skill, schema: 1, version, files }, null, 2) + '\n');
    // Recheck immediately before replacing an installation that may have changed while copying.
    const latest = await managedState(target, recordFor(skill));
    if (JSON.stringify(latest) !== JSON.stringify(previous)) throw new Error(`Installation changed during preparation: ${target}`);
    if (previous) await fs.rename(target, backup);
    try { await fs.rename(incoming, target); }
    catch (error) {
      if (previous) {
        try { await fs.rename(backup, target); }
        catch (restoreError) {
          preserveBackup = true;
          throw new Error(`Replacement failed; original preserved at ${backup}. Restore failed: ${restoreError.message}`, { cause: error });
        }
      }
      throw error;
    }
    return previous ? 'Updated' : 'Installed';
  } finally {
    if (!preserveBackup) await fs.rm(staging, { recursive: true, force: true });
  }
}

export async function uninstall(target, skill) {
  const record = recordFor(skill);
  if (!await managedState(target, record)) return 'Not installed';
  const holding = await fs.mkdtemp(path.join(path.dirname(target), `.${owner}-remove-`));
  const backup = path.join(holding, 'installed');
  let moved = false;
  try {
    await fs.rename(target, backup);
    moved = true;
    // Verify the moved tree as well before deleting any user-visible content.
    await managedState(backup, record);
  } catch (error) {
    if (moved) await fs.rename(backup, target);
    await fs.rm(holding, { recursive: true, force: true });
    throw error;
  }
  await fs.rm(holding, { recursive: true });
  return 'Uninstalled';
}
