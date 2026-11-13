# Git Hooks

[English](README.md) | [한국어](README.ko.md)

건너뛸 이유가 없을 만큼 빠른 Git 훅을 세팅하고, 점검하고, 문제를 해결하는 에이전트 스킬입니다. 결과는 실제 커밋과 push로 검증합니다.

## 하는 일

원하는 검사를 말하면 됩니다. 예를 들면:

> 커밋 전에 린트랑 시크릿 검사가 돌게 해 주시고, 팀원들도 클론하면 같이 쓰게 해 주세요.

스킬은 저장소를 살펴보고, 맞는 훅 도구를 고르고, 검사를 알맞은 훅에 배치한 뒤 실제 Git 명령으로 결과를 확인합니다. 최종 보고에는 고른 도구와 이유, 실행해 본 시나리오, 긴급 우회 방법, 서버 쪽에서 따로 막아야 할 것이 들어갑니다.

| 상황 | 보통 고르는 도구 |
| --- | --- |
| 추가 의존성을 원하지 않음 | Git 내장 `core.hooksPath`와 저장소에 커밋한 `.githooks/` 폴더 |
| 여러 언어, 모노레포 | Lefthook |
| Python 중심 | `pre-commit` 또는 `prek` |
| Node.js 단일 패키지 | Husky와 `lint-staged`, `commitlint` |

배치할 수 있는 검사:

- **pre-commit:** staged 내용만 보는 시크릿 검사(gitleaks가 있으면 사용, 없으면 내장 패턴), `.env`·키 파일, 병합 충돌 표시, 큰 파일, 대소문자만 다른 파일 이름, 바뀐 파일 린트. 자동 수정 포매터를 넣을 때는 staged하지 않은 변경이 커밋에 섞이지 않게 하고, 일부만 stage한 파일로 이를 확인합니다.
- **commit-msg:** Conventional Commits 형식. 제목 길이를 바이트가 아니라 글자 수로 세서 한글 제목이 일찍 막히지 않습니다.
- **prepare-commit-msg (요청 시):** 브랜치 이름의 이슈 키를 트레일러로 추가합니다.
- **pre-push (요청 시):** 명시적 우회가 있는 보호 브랜치, `WIP`/`fixup!` 커밋, 새 브랜치의 첫 push 처리.
- **post-checkout / post-merge (요청 시):** lockfile이나 마이그레이션이 바뀌면 알려 줍니다.

Codex에서는 `$git-hooks`, Claude Code에서는 `/git-hooks`로 부르거나 할 일만 설명하면 됩니다. 훅별 인자와 흔한 실수는 [훅 카탈로그(영어)](references/hook-catalog.md)에 있습니다.

## 실행하는 것과 바꾸는 것

- 에이전트는 저장소에 훅 파일과 훅 도구 설정을 쓰고, 저장소 로컬 Git 설정에 `core.hooksPath`를 지정합니다. 전역 Git 설정은 바꾸지 않습니다.
- [`scripts/install-hooks.sh`](scripts/install-hooks.sh)는 [`examples/githooks/`](examples/githooks/)의 POSIX 훅 6개를 `<repo>/.githooks/`로 복사하고 `core.hooksPath`를 지정합니다. 같은 이름의 기존 파일은 덮어씁니다.
- 훅에는 `git`과 POSIX 셸이 필요합니다. gitleaks, Lefthook, `pre-commit`은 선택 사항이며 설치되어 있거나 선택했을 때만 씁니다.
- 검증을 위해 테스트 커밋을 만들고, `pre-push`는 로컬 bare 원격을 만들어 시험한 뒤 만든 것을 정리합니다.

## 설치

Node.js 22.14 이상이 필요합니다.

```sh
npx @tortle1228/agent-skills@latest install --agent all --skill git-hooks
```

별도 Skills CLI로 GitHub에서 설치할 수도 있습니다.

```sh
npx skills add tortle1228/agent-skills --skill git-hooks -g -a codex -a claude-code
```

npm 설치기는 Codex와 Claude Code를 지원합니다. Antigravity, Gemini CLI, GitHub Copilot, Cursor, Windsurf, OpenCode처럼 Agent Skills(`SKILL.md`)를 읽는 다른 에이전트에는 Skills CLI에 해당 에이전트 이름을 붙여 설치합니다(예: `-a cursor`).

호스트마다 한 가지 설치 방식만 쓰세요. 설치본은 `~/.agents/skills/git-hooks`(Codex)와 `~/.claude/skills/git-hooks`(Claude Code)에 있습니다.

## 갱신과 제거

새 버전 패키지로 설치 명령을 다시 실행하면 갱신됩니다. 직접 수정한 설치본은 충돌로 보고하고 건드리지 않습니다. 스킬을 제거해도 저장소에 이미 설치한 훅은 지워지지 않습니다.

```sh
npx @tortle1228/agent-skills@latest uninstall --agent all --skill git-hooks
```

## 라이선스

[MIT](LICENSE).
