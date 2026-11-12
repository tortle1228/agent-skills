import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';

// Usage: node scripts/check-docs.js            -> whole repository
//        node scripts/check-docs.js <skillDir> -> one installed skill (links must stay inside it)
async function walk(dir) {
  const result = [];
  for (const item of await fs.readdir(dir, { withFileTypes: true })) {
    // evals/ holds Korean test prompts and fixtures; it is not shipped.
    if (['.git', 'node_modules', 'evals'].includes(item.name)) continue;
    const file = path.join(dir, item.name);
    if (item.isDirectory()) result.push(...await walk(file));
    else if (item.name.endsWith('.md')) result.push(file);
  }
  return result;
}

const read = async file => (await fs.readFile(file, 'utf8')).replaceAll('\r\n', '\n');

// Checks fences, local links, JSON blocks and language placement. Links may not leave `boundary`.
// `licenseFrom` lets a skill link to the LICENSE the installer adds at its root.
async function checkTree(dir, boundaryFor, licenseFrom) {
  let count = 0;
  for (const file of await walk(dir)) {
    const text = await read(file);
    let fence = null;
    const rendered = text.split('\n').filter(line => {
      const match = line.match(/^\s*(`{3,}|~{3,})/);
      if (match) {
        if (!fence) fence = match[1];
        else if (match[1][0] === fence[0] && match[1].length >= fence.length) fence = null;
        return false;
      }
      return !fence;
    }).join('\n');
    assert.equal(fence, null, `Unclosed fence: ${file}`);
    const boundary = boundaryFor(file);
    const urls = [...rendered.matchAll(/!?\[[^\]]*\]\(([^)]+)\)|(?:src|srcset)="([^"]+)"/g)].map(m => m[1] || m[2]);
    for (const url of urls) {
      if (/^[a-z]+:|^#/i.test(url)) continue;
      const target = path.resolve(path.dirname(file), decodeURIComponent(url.split('#')[0]));
      assert.ok(target === boundary || target.startsWith(boundary + path.sep), `Link escapes ${path.relative(dir, boundary) || 'package'}: ${file}: ${url}`);
      const provided = licenseFrom && target === path.join(boundary, 'LICENSE') ? licenseFrom : target;
      await fs.access(provided).catch(() => { throw new Error(`Broken link: ${file}: ${url}`); });
      count++;
    }
    // agent-code-review deliberately shows Korean report labels as examples.
    const koreanExamples = [path.join('agent-code-review', 'references', 'report-format.md'), path.join('agent-code-review', 'SKILL.md')];
    if (!file.endsWith('README.ko.md') && !koreanExamples.some(example => file.endsWith(example))) {
      assert.ok(!/[가-힣]/.test(text.replaceAll('한국어', 'Korean')), `Untranslated text: ${file}`);
    }
    for (const m of text.matchAll(/```json\n([\s\S]*?)\n```/g)) JSON.parse(m[1]);
  }
  return count;
}

async function checkSkillMd(skillDir) {
  const name = path.basename(skillDir);
  const skill = await read(path.join(skillDir, 'SKILL.md'));
  const front = skill.match(/^---\n([\s\S]*?)\n---\n/);
  assert.ok(front, `Missing frontmatter: ${name}`);
  assert.match(front[1], new RegExp(`^name: ${name}$`, 'm'), `Frontmatter name must match folder: ${name}`);
  assert.match(front[1], /^description: (?:\S.*|>-\n(?: {2}.+\n?)+)$/m, `Missing description: ${name}`);
}

const links = text => [...new Set([...text.matchAll(/\]\(([^)]+)\)/g)].map(m => m[1]))].sort();
async function checkParity(dir) {
  const korean = await read(path.join(dir, 'README.ko.md')).catch(() => null);
  if (korean !== null) assert.deepEqual(links(await read(path.join(dir, 'README.md'))), links(korean), `README link parity: ${dir}`);
}

if (process.argv[2]) {
  const skillDir = path.resolve(process.argv[2]);
  await checkSkillMd(skillDir);
  const count = await checkTree(skillDir, () => skillDir);
  console.log(`Installed skill checks passed: ${path.basename(skillDir)}, ${count} local links/assets.`);
} else {
  const root = process.cwd();
  const skillsRoot = path.join(root, 'skills');
  const skills = (await fs.readdir(skillsRoot, { withFileTypes: true })).filter(e => e.isDirectory()).map(e => e.name);
  const boundaryFor = file => {
    const relative = path.relative(skillsRoot, file);
    return relative.startsWith('..') ? root : path.join(skillsRoot, relative.split(path.sep)[0]);
  };
  const count = await checkTree(root, boundaryFor, path.join(root, 'LICENSE'));
  for (const skill of skills) {
    await checkSkillMd(path.join(skillsRoot, skill));
    await checkParity(path.join(skillsRoot, skill));
  }
  await checkParity(root);
  const writer = path.join(skillsRoot, 'readme-writer');
  for (const type of ['swift-package', 'cli', 'app', 'mcp-server', 'coding-agent', 'skill-package', 'pi-package']) {
    assert.ok((await read(path.join(writer, 'examples', type, 'README.md'))).includes('Fictional documentation example'));
    await read(path.join(writer, 'examples', type, 'EXPLAIN.md'));
    assert.ok((await read(path.join(writer, 'templates', `${type}.md`))).includes('REPLACE'));
  }
  assert.match(await read(path.join(root, 'LICENSE')), /MIT License/);
  console.log(`Documentation checks passed: ${skills.length} skills, ${count} local links/assets, seven readme-writer example/template pairs.`);
}
