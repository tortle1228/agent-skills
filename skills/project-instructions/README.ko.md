# Project Instructions

[English](README.md) | [한국어](README.ko.md)

코딩 에이전트가 읽는 지침 파일을 만들고, 점검하고, 줄이고, 서로 맞춰 주는 에이전트 스킬입니다. `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`와 Claude Code·Antigravity·Cursor·Copilot·Windsurf의 규칙 폴더를 다룹니다.

## 하는 일

| 모드 | 요청 예시 | 결과 |
| --- | --- | --- |
| 새로 만들기 | "이 저장소에 AGENTS.md를 만들고 Claude Code에서도 읽히게 해 주세요." | 검증한 명령과 프로젝트 고유 규칙만 담은 짧은 `AGENTS.md`, 그리고 `@AGENTS.md`로 불러오는 `CLAUDE.md` |
| 점검과 다이어트 | "에이전트 지침이 길고 서로 안 맞아요. 정리해 주세요." | 낡은 명령과 경로 수정, 일반론과 포매팅 규칙 삭제, 실제 규칙 유지, 변경 전후 요약 |
| 동기화 | "CLAUDE.md, .cursorrules, Copilot 지침을 맞춰 주세요." | `AGENTS.md`를 유일한 원본으로 두고 도구별로 얇게 연결 |
| 갱신 | "에이전트가 같은 실수를 반복해요. 규칙을 추가해 주세요." | 가장 싸고 확실한 해결책: 린트 규칙, 훅, 범위별 규칙, 또는 `AGENTS.md`에 한두 줄 |

[내용 기준(영어)](references/content-rubric.md)의 원칙을 따릅니다. 지웠을 때 에이전트가 코드만 읽고는 피할 수 없는 실수가 생길 줄만 남기고, 포매팅은 린터에 맡기고, 원본은 하나로 유지합니다.

지침 파일은 대화 언어가 아니라 저장소에서 이미 쓰는 언어로 씁니다(근거가 없으면 영어). 요청한 파일만 바꾸고, 훅이나 다른 도구용 파일은 요청하지 않으면 만들지 않고 보고서에서 제안합니다.

Codex에서는 `$project-instructions`, Claude Code에서는 `/project-instructions`로 부르거나 할 일만 설명하면 됩니다.

## 실행하는 것과 바꾸는 것

- [`scripts/audit_instructions.py`](scripts/audit_instructions.py)는 읽기 전용 정적 감사기입니다(Python 3 표준 라이브러리만 사용). 없는 패키지 스크립트와 Make 타깃, 깨진 경로와 import, lockfile 불일치, 빠진 frontmatter, 연결되지 않은 중복, 지나치게 큰 파일, 로컬 경로 하드코딩, 비밀값으로 보이는 문자열을 찾습니다. 직접 실행하려면 `python3 scripts/audit_instructions.py <repo> [--json] [--strict]`입니다.
- 에이전트는 저장소의 지침 파일을 수정합니다. 오래된 파일을 지우거나 큰 섹션을 잘라 낼 때는 계획을 먼저 보여 주고 물어봅니다. 지워진 규칙에 팀만 아는 지식이 담겨 있을 수 있기 때문입니다.

## 설치

설치기에는 Node.js 22.14 이상, 감사기에는 Python 3가 필요합니다.

```sh
npx @tortle1228/agent-skills@latest install --agent all --skill project-instructions
```

별도 Skills CLI로 GitHub에서 설치할 수도 있습니다.

```sh
npx skills add tortle1228/agent-skills --skill project-instructions -g -a codex -a claude-code
```

npm 설치기는 Codex와 Claude Code를 지원합니다. Antigravity, Gemini CLI, GitHub Copilot, Cursor, Windsurf, OpenCode처럼 Agent Skills(`SKILL.md`)를 읽는 다른 에이전트에는 Skills CLI에 해당 에이전트 이름을 붙여 설치합니다(예: `-a cursor`).

호스트마다 한 가지 설치 방식만 쓰세요. 설치본은 `~/.agents/skills/project-instructions`(Codex)와 `~/.claude/skills/project-instructions`(Claude Code)에 있습니다.

## 갱신과 제거

새 버전 패키지로 설치 명령을 다시 실행하면 갱신됩니다. 직접 수정한 설치본은 충돌로 보고하고 건드리지 않습니다.

```sh
npx @tortle1228/agent-skills@latest uninstall --agent all --skill project-instructions
```

## 라이선스

[MIT](LICENSE).
