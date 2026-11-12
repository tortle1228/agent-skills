#!/usr/bin/env node
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { install, uninstall, listSkills, targetFor } from '../lib/installer.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const { version } = JSON.parse(await fs.readFile(path.join(root, 'package.json'), 'utf8'));
const available = await listSkills(root);
const args = process.argv.slice(2);
const help = `Agent Skills ${version}

Usage:
  agent-skills install --agent codex|claude-code|all [--skill <name> ...]
  agent-skills uninstall --agent codex|claude-code|all [--skill <name> ...]
  agent-skills list
  agent-skills --version

Skills: ${available.join(', ')}
Without --skill, every skill is selected. Repeat --skill to choose several.
Existing unmanaged or modified files are never overwritten.
Run install from a newer package version to update. No arguments makes no changes.`;

function parse(rest) {
  let agent;
  const skills = [];
  for (let i = 0; i < rest.length; i += 2) {
    const [flag, value] = [rest[i], rest[i + 1]];
    if (value === undefined) return null;
    if (flag === '--agent' && agent === undefined) agent = value;
    else if (flag === '--skill') skills.push(value);
    else return null;
  }
  if (!['codex', 'claude-code', 'all'].includes(agent)) return null;
  return { agents: agent === 'all' ? ['codex', 'claude-code'] : [agent], skills: skills.length ? [...new Set(skills)] : available };
}

const command = args[0];
const options = ['install', 'uninstall'].includes(command) ? parse(args.slice(1)) : null;
if (!args.length || (args.length === 1 && ['--help', '-h'].includes(command))) console.log(help);
else if (args.length === 1 && command === '--version') console.log(version);
else if (args.length === 1 && command === 'list') console.log(available.join('\n'));
else if (!options) {
  console.error(help);
  process.exitCode = 1;
} else if (options.skills.some(skill => !available.includes(skill))) {
  console.error(`Unknown skill: ${options.skills.filter(skill => !available.includes(skill)).join(', ')}\nAvailable: ${available.join(', ')}`);
  process.exitCode = 1;
} else {
  for (const agent of options.agents) {
    for (const skill of options.skills) {
      const target = targetFor(os.homedir(), agent, skill);
      try {
        const result = command === 'install' ? await install(root, skill, target, version) : await uninstall(target, skill);
        console.log(`${agent}/${skill}: ${result} — ${target}`);
      } catch (error) {
        console.error(`${agent}/${skill}: ${error.message}`);
        process.exitCode = 1;
      }
    }
  }
}
