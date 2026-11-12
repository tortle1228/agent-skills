import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import assert from 'node:assert/strict';
import { pathToFileURL } from 'node:url';
import { execFileSync } from 'node:child_process';
const root = process.cwd();
const temporary = await fs.mkdtemp(path.join(os.tmpdir(), 'agent-skills-pack-'));
try {
  const npm = process.platform === 'win32' ? 'npm.cmd' : 'npm';
  const output = execFileSync(npm, ['pack', '--json', '--ignore-scripts', '--pack-destination', temporary], {
    cwd: root, encoding: 'utf8', shell: process.platform === 'win32'
  });
  const pack = JSON.parse(output)[0];
  const allowed = /^(bin\/|lib\/|skills\/[a-z0-9-]+\/|README(?:\.ko)?\.md$|LICENSE$|CHANGELOG\.md$|CONTRIBUTING\.md$|package\.json$)/;
  for (const file of pack.files) {
    assert.ok(allowed.test(file.path) && !file.path.includes('.DS_Store'), `Unexpected packed file: ${file.path}`);
  }
  execFileSync('tar', ['-xzf', path.join(temporary, pack.filename), '-C', temporary]);
  const unpacked = path.join(temporary, 'package');
  const { version } = JSON.parse(await fs.readFile(path.join(unpacked, 'package.json')));
  const cli = path.join(unpacked, 'bin/agent-skills.js');
  assert.equal(execFileSync(process.execPath, [cli, '--version'], { encoding: 'utf8' }).trim(), version);
  const skills = execFileSync(process.execPath, [cli, 'list'], { encoding: 'utf8' }).trim().split('\n');
  assert.deepEqual(skills, ['agent-code-review', 'create-verification', 'git-hooks', 'project-bootstrap', 'project-instructions', 'readme-writer', 'verification']);
  // Run the packed installer, with a temporary home injected only into this test process.
  const home = path.join(temporary, 'home');
  const preload = path.join(temporary, 'home.mjs');
  await fs.writeFile(preload, `import os from 'node:os'; os.homedir = () => ${JSON.stringify(home)};`);
  execFileSync(process.execPath, ['--import', pathToFileURL(preload).href, cli, 'install', '--agent', 'all']);
  await fs.rm(unpacked, { recursive: true });
  for (const host of ['.agents', '.claude']) {
    for (const skill of skills) {
      const dir = path.join(home, host, 'skills', skill);
      execFileSync(process.execPath, [path.join(root, 'scripts/check-docs.js'), dir]);
      await fs.access(path.join(dir, 'LICENSE'));
      await assert.rejects(fs.access(path.join(dir, 'evals')), { code: 'ENOENT' });
    }
    // Skill scripts and hook templates must stay executable after npm pack and install.
    if (process.platform !== 'win32') {
      for (const file of ['git-hooks/scripts/install-hooks.sh', 'git-hooks/examples/githooks/pre-commit', 'project-bootstrap/scripts/audit-project.sh']) {
        assert.ok((await fs.stat(path.join(home, host, 'skills', file))).mode & 0o111, `Not executable after install: ${file}`);
      }
    }
  }
  console.log(`Packed ${pack.files.length} allowed files; CLI and cache-independent installation of ${skills.length} skills passed.`);
} finally { await fs.rm(temporary, { recursive: true, force: true }); }
