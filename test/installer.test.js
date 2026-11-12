import { test, mock } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { execFileSync, spawnSync } from 'node:child_process';
import { install, uninstall, listSkills, targetFor } from '../lib/installer.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const skill = 'readme-writer';
const marker = '.agent-skills-install.json';
async function fixture(t) {
  const home = await fs.mkdtemp(path.join(os.tmpdir(), 'agent-skills-test-'));
  t.after(() => fs.rm(home, { recursive: true, force: true }));
  return { home, target: targetFor(home, 'codex', skill) };
}
async function cli(home) {
  const preload = path.join(home, 'home.mjs');
  await fs.writeFile(preload, `import os from 'node:os'; os.homedir = () => ${JSON.stringify(home)};`);
  return ['--import', pathToFileURL(preload).href, path.join(root, 'bin/agent-skills.js')];
}

test('every skill folder is listed and installable', async t => {
  const { home } = await fixture(t);
  const skills = await listSkills(root);
  assert.deepEqual(skills, ['agent-code-review', 'create-verification', 'git-hooks', 'project-bootstrap', 'project-instructions', 'readme-writer', 'verification']);
  for (const name of skills) {
    const target = targetFor(home, 'claude-code', name);
    assert.equal(await install(root, name, target, '0.1.0'), 'Installed');
    assert.match(await fs.readFile(path.join(target, 'SKILL.md'), 'utf8'), new RegExp(`name: ${name}`));
    await fs.access(path.join(target, 'LICENSE'));
    await assert.rejects(fs.access(path.join(target, 'evals')), { code: 'ENOENT' });
  }
});

test('install, idempotence, version upgrade, and remove preserve unrelated files', async t => {
  const { home, target } = await fixture(t);
  await fs.writeFile(path.join(home, 'keep.txt'), 'keep');
  assert.equal(await install(root, skill, target, '0.1.0'), 'Installed');
  assert.equal(await install(root, skill, target, '0.1.0'), 'Already installed');
  assert.equal(await install(root, skill, target, '0.1.1'), 'Updated');
  assert.equal(JSON.parse(await fs.readFile(path.join(target, marker))).version, '0.1.1');
  assert.equal(await uninstall(target, skill), 'Uninstalled');
  assert.equal(await uninstall(target, skill), 'Not installed');
  assert.equal(await fs.readFile(path.join(home, 'keep.txt'), 'utf8'), 'keep');
});

test('a record for another skill is not accepted', async t => {
  const { home, target } = await fixture(t);
  await install(root, skill, target, '0.1.0');
  const other = targetFor(home, 'codex', 'project-bootstrap');
  await fs.cp(target, other, { recursive: true });
  await assert.rejects(install(root, 'project-bootstrap', other, '0.1.0'), /Unrecognized/);
  await assert.rejects(uninstall(other, 'project-bootstrap'), /Unrecognized/);
});

test('edits and added files block update and removal', async t => {
  const { target } = await fixture(t);
  await install(root, skill, target, '0.1.0');
  await fs.appendFile(path.join(target, 'SKILL.md'), '\nMy edits\n');
  await assert.rejects(install(root, skill, target, '0.2.0'), /Locally modified/);
  await assert.rejects(uninstall(target, skill), /Locally modified/);
  assert.match(await fs.readFile(path.join(target, 'SKILL.md'), 'utf8'), /My edits/);
});

test('unknown directories and symlinks are never replaced', async t => {
  const { home, target } = await fixture(t);
  await fs.mkdir(target, { recursive: true });
  await fs.writeFile(path.join(target, 'mine'), 'mine');
  await assert.rejects(install(root, skill, target, '0.1.0'), /Unmanaged/);
  await assert.rejects(uninstall(target, skill), /Unmanaged/);
  const link = path.join(home, 'linked');
  await fs.symlink(target, link, process.platform === 'win32' ? 'junction' : 'dir');
  await assert.rejects(install(root, skill, link, '0.1.0'), /symlink/);
  await assert.rejects(uninstall(link, skill), /symlink/);
  assert.equal(await fs.readFile(path.join(target, 'mine'), 'utf8'), 'mine');
});

test('replacement failure restores the previous installation', async t => {
  const { target } = await fixture(t);
  await install(root, skill, target, '0.1.0');
  const original = fs.rename;
  const replacement = mock.method(fs, 'rename', async (from, to) => {
    if (path.basename(from) === 'incoming' && to === target) throw new Error('Injected replacement failure');
    return original(from, to);
  });
  try { await assert.rejects(install(root, skill, target, '0.2.0'), /Injected replacement failure/); }
  finally { replacement.mock.restore(); }
  assert.equal(JSON.parse(await fs.readFile(path.join(target, marker))).version, '0.1.0');
  assert.equal(await install(root, skill, target, '0.1.0'), 'Already installed');
});

test('blocked parent fails without touching its contents', async t => {
  const { home } = await fixture(t);
  const parent = path.join(home, 'file');
  await fs.writeFile(parent, 'original');
  await assert.rejects(install(root, skill, path.join(parent, 'skill'), '0.1.0'));
  assert.equal(await fs.readFile(parent, 'utf8'), 'original');
});

test('unrecognized ownership record and deleted files are refused', async t => {
  const { target } = await fixture(t);
  await install(root, skill, target, '0.1.0');
  await fs.unlink(path.join(target, 'LICENSE'));
  await assert.rejects(uninstall(target, skill), /Locally modified/);
  await fs.writeFile(path.join(target, marker), '{bad');
  await assert.rejects(install(root, skill, target, '0.2.0'), /Unmanaged/);
});

test('CLI help is non-mutating, validates input, and reports partial failure', async t => {
  const { home } = await fixture(t);
  const args = await cli(home);
  assert.match(execFileSync(process.execPath, args, { encoding: 'utf8' }), /Usage:/);
  await assert.rejects(fs.stat(path.join(home, '.agents')), { code: 'ENOENT' });
  assert.equal(spawnSync(process.execPath, [...args, 'install', '--agent', 'unknown']).status, 1);
  assert.equal(spawnSync(process.execPath, [...args, 'install', '--agent', 'codex', '--skill']).status, 1);
  const unknown = spawnSync(process.execPath, [...args, 'install', '--agent', 'codex', '--skill', 'nope'], { encoding: 'utf8' });
  assert.equal(unknown.status, 1);
  assert.match(unknown.stderr, /Available: agent-code-review, create-verification, git-hooks, project-bootstrap, project-instructions, readme-writer, verification/);
  await assert.rejects(fs.stat(path.join(home, '.agents')), { code: 'ENOENT' });
  const blocked = targetFor(home, 'codex', skill);
  await fs.mkdir(blocked, { recursive: true });
  await fs.writeFile(path.join(blocked, 'mine'), 'preserved');
  const result = spawnSync(process.execPath, [...args, 'install', '--agent', 'all', '--skill', skill], { encoding: 'utf8' });
  assert.equal(result.status, 1);
  assert.match(result.stderr, /Unmanaged/);
  assert.match(result.stdout, /claude-code\/readme-writer: Installed/);
  assert.equal(await fs.readFile(path.join(blocked, 'mine'), 'utf8'), 'preserved');
});

test('CLI --skill installs only the chosen skills', async t => {
  const { home } = await fixture(t);
  const args = await cli(home);
  const result = spawnSync(process.execPath, [...args, 'install', '--agent', 'claude-code', '--skill', 'project-bootstrap', '--skill', skill], { encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr);
  assert.deepEqual((await fs.readdir(path.join(home, '.claude', 'skills'))).sort(), ['project-bootstrap', 'readme-writer']);
  await assert.rejects(fs.stat(path.join(home, '.agents')), { code: 'ENOENT' });
  const removed = spawnSync(process.execPath, [...args, 'uninstall', '--agent', 'claude-code'], { encoding: 'utf8' });
  assert.equal(removed.status, 0, removed.stderr);
  assert.match(removed.stdout, /agent-code-review: Not installed/);
  assert.deepEqual(await fs.readdir(path.join(home, '.claude', 'skills')), []);
});
