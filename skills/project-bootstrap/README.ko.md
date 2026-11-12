# Project Bootstrap

[English](README.md) | [한국어](README.ko.md)

새 프로젝트를 시작하거나 기존 저장소를 10대 엔지니어링 영역 기준으로 점검하는 에이전트 스킬입니다. 무조건 많이 갖추기보다 프로젝트 규모에 맞춰 구성합니다.

## 하는 일

요청을 보고 세 가지 모드 중 하나를 고릅니다.

| 모드 | 요청 예시 | 결과 |
| --- | --- | --- |
| 새 프로젝트 | "마크다운 단어 수를 세는 작은 Python CLI를 세팅해 주세요." | 공식 생성기로 만든 골격과 런타임 고정, lockfile, 포매터, 린터, 타입 검사, 통과하는 테스트 1개, `.gitignore`, `AGENTS.md`. 검증 명령은 실제로 실행합니다 |
| 기존 저장소 | "이 저장소 셋업에서 빠진 게 뭔지 보고서만 써 주세요." | P0/P1/P2로 나눈 개선 항목과 단계별 도입 계획. 요청하지 않으면 아무것도 바꾸지 않습니다 |
| 자문 | "우리 팀엔 FastAPI, DRF, Litestar 중 뭐가 맞을까요?" | 가중치 평가표, 추천 1개, 그 선택이 맞지 않는 경우, 원하면 ADR |

새 프로젝트는 세 가지 프리셋 중 하나로 만듭니다. 프로토타입과 개인 도구는 **Lean MVP**, 실제 서비스는 **Standard Production**(기본값), 여러 팀이 쓰거나 규제가 있는 시스템은 **Strict Enterprise**입니다. 프리셋별 포함 항목은 [체크리스트(영어)](references/10-pillars-checklist.md)에 있습니다.

Codex에서는 `$project-bootstrap`, Claude Code에서는 `/project-bootstrap`으로 부릅니다. 할 일만 설명해도 지원 호스트가 스킬 설명을 보고 자동으로 고를 수 있습니다.

## 실행하는 것과 바꾸는 것

- [`scripts/audit-project.sh`](scripts/audit-project.sh)는 읽기만 합니다. 설치된 런타임과 영역별 설정 파일 유무를 보여 줍니다. `pyproject.toml`·`package.json` 안에 있는 설정과 Rust·Go의 내장 도구도 인식합니다. `bash`가 필요합니다.
- 새 프로젝트 모드에서는 공식 생성기(`uv init`, `pnpm create …`, `cargo init` 등)를 실행하고, 프로젝트 안에 의존성을 설치하고, 검증 명령을 돌립니다. 필요한 런타임이 없으면 git이 무시하는 폴더에 임시 툴체인을 받아 검증한 뒤 지웁니다. 동의 없이 시스템 전역이나 `sudo`로 설치하지 않습니다.
- Git 훅과 에이전트 지침 파일은 형제 스킬인 `git-hooks`와 `project-instructions`가 설치되어 있으면 그쪽에 맡깁니다. 없으면 최소한의 pre-commit 훅과 짧은 `AGENTS.md`를 직접 만듭니다.
- 도구 추천은 금방 낡습니다. 참고 파일만 믿지 않고, 호스트가 제공하면 Context7이나 웹 검색으로 공식 문서의 현재 버전을 확인합니다.

## 설치

Node.js 22.14 이상이 필요합니다. 이 스킬만 두 호스트에 설치합니다.

```sh
npx @tortle1228/agent-skills@latest install --agent all --skill project-bootstrap
```

위임 대상 스킬도 함께 설치하려면 `--skill git-hooks --skill project-instructions`를 덧붙입니다. 별도 Skills CLI로 GitHub에서 설치할 수도 있습니다.

```sh
npx skills add tortle1228/agent-skills --skill project-bootstrap -g -a codex -a claude-code
```

npm 설치기는 Codex와 Claude Code를 지원합니다. Antigravity, Gemini CLI, GitHub Copilot, Cursor, Windsurf, OpenCode처럼 Agent Skills(`SKILL.md`)를 읽는 다른 에이전트에는 Skills CLI에 해당 에이전트 이름을 붙여 설치합니다(예: `-a cursor`).

호스트마다 한 가지 설치 방식만 쓰세요. 설치본은 `~/.agents/skills/project-bootstrap`(Codex)와 `~/.claude/skills/project-bootstrap`(Claude Code)에 있습니다.

## 갱신과 제거

새 버전 패키지로 설치 명령을 다시 실행하면 갱신됩니다. 직접 수정한 설치본은 충돌로 보고하고 건드리지 않습니다.

```sh
npx @tortle1228/agent-skills@latest uninstall --agent all --skill project-bootstrap
```

## 라이선스

[MIT](LICENSE).
