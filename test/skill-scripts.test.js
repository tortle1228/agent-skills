import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const hasPython = spawnSync('python3', ['--version']).status === 0;

test('project-instructions auditor passes its fixture tests', t => {
  if (!hasPython) return t.skip('python3 is not on PATH');
  const result = spawnSync('python3', ['test/project_instructions_audit.py', 'skills/project-instructions/scripts/audit_instructions.py'], { cwd: root, encoding: 'utf8' });
  assert.equal(result.status, 0, `${result.stdout}\n${result.stderr}`);
});

const has = cmd => spawnSync(cmd, ['--version']).status === 0;

test('git-hooks e2e scenarios pass in a temporary repository', t => {
  if (process.platform === 'win32') return t.skip('POSIX hooks are not tested on Windows');
  if (!has('bash') || !has('git')) return t.skip('bash or git is not on PATH');
  const result = spawnSync('bash', ['test/git_hooks_e2e.sh', 'skills/git-hooks'], { cwd: root, encoding: 'utf8' });
  assert.equal(result.status, 0, `${result.stdout}\n${result.stderr}`);
});

test('project-bootstrap audit script finds settings kept inside manifests', async t => {
  if (process.platform === 'win32' || !has('bash')) return t.skip('bash is not available');
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), 'agent-skills-audit-'));
  t.after(() => fs.rm(dir, { recursive: true, force: true }));
  await fs.writeFile(path.join(dir, 'requirements.txt'), 'flask\n');
  await fs.writeFile(path.join(dir, 'pyproject.toml'), '[tool.ruff]\nline-length = 100\n[tool.pytest.ini_options]\ntestpaths = ["tests"]\n');
  const result = spawnSync('bash', ['skills/project-bootstrap/scripts/audit-project.sh', dir], { cwd: root, encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /\[OK\]\s+Pillar 1: Package Manifest\s+-> .*requirements\.txt/);
  assert.match(result.stdout, /\[OK\]\s+Pillar 4: Format \/ Lint \/ Types\s+-> pyproject\.toml\[ruff\]/);
  assert.match(result.stdout, /\[OK\]\s+Pillar 5: Testing Config\s+-> pyproject\.toml\[pytest\]/);
  assert.match(result.stdout, /\[NONE\]\s+Pillar 1: Lockfile/);
});

test('project-bootstrap audit script counts Rust built-in tooling', async t => {
  if (process.platform === 'win32' || !has('bash')) return t.skip('bash is not available');
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), 'agent-skills-audit-'));
  t.after(() => fs.rm(dir, { recursive: true, force: true }));
  await fs.writeFile(path.join(dir, 'Cargo.toml'), '[package]\nname = "x"\nversion = "0.1.0"\n');
  const result = spawnSync('bash', ['skills/project-bootstrap/scripts/audit-project.sh', dir], { cwd: root, encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /\[OK\]\s+Pillar 4: Format \/ Lint \/ Types\s+-> Cargo\.toml\[built-in: rustfmt,clippy\]/);
  assert.match(result.stdout, /\[OK\]\s+Pillar 5: Testing Config\s+-> Cargo\.toml\[built-in: cargo test\]/);
});
