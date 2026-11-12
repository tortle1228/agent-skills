# Maintenance and review

[Home](../README.md)

## Update documentation with behavior

| Change | Recheck |
| --- | --- |
| Installation, distribution, minimum version | Getting started, compatibility, templates, translations |
| Public API, tools, commands | Minimal examples, input/output, detailed reference |
| Storage, transfer, permissions, automatic configuration | Data handling, limitations, removal/restoration |
| UI or workflow | Images, alt text, first-use instructions |
| License decision or third-party asset | Actual license, README summary, attribution and scope |

Keep each fact in one canonical place and link it elsewhere. Avoid unnecessary repetition of versions and feature counts. Update supported behavior and limitations across translations in the same change.

## Completion checklist

- [ ] A newcomer can explain the project's purpose.
- [ ] Prerequisites appear before the task that needs them.
- [ ] Working directory, command, and expected result connect.
- [ ] Verified facts and untested claims are distinguished.
- [ ] Links, images, code blocks, tables, and collapsed sections work.
- [ ] Affected translations and screenshots were updated.
- [ ] No unsupported performance, compatibility, or license claim was added.

Check redirects as well as external URLs. Link checks are not installation or browser compatibility tests. State the renderer used: local preview is not proof of GitHub rendering.

## Add research deliberately

Explain what a README teaches, not how popular its project is. Read the source, record the URL/date/observed section, and separate observations from recommendations. Prefer commit links for stable evidence. Mark unread linked resources as further reading and merge duplicate examples.

[Awesome README's contribution rules](https://github.com/matiassingers/awesome-readme/blob/master/contributing.md) focus descriptions on the README and check duplicates/links. Its human-written-description rule governs contributions there; it is not a universal ban on AI here.
