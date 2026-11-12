# Agent Skills

[English](README.md) | [한국어](README.ko.md)

코드 주변의 일상적인 엔지니어링 작업을 다루는 에이전트 스킬 5개입니다. 프로젝트 시작, 에이전트 지침, Git 훅, 코드 리뷰, README를 다룹니다. 전부 설치하거나 필요한 것만 골라 설치할 수 있습니다.

## 스킬

| 스킬 | 쓰임 |
| --- | --- |
| [project-bootstrap](skills/project-bootstrap/README.md) | 프로젝트를 시작하거나 저장소 셋업을 10대 영역 기준으로 규모에 맞게 점검합니다. 스택을 비교하고 결정을 기록합니다 |
| [project-instructions](skills/project-instructions/README.md) | `AGENTS.md`, `CLAUDE.md` 등 에이전트 규칙 파일을 만들고, 줄이고, 맞춥니다. 낡은 명령과 경로를 찾는 정적 감사기가 들어 있습니다 |
| [git-hooks](skills/git-hooks/README.md) | 팀이 함께 쓰는 빠른 pre-commit, commit-msg, pre-push 훅을 세팅하고 실제 커밋으로 검증합니다 |
| [agent-code-review](skills/agent-code-review/README.md) | 분리된 리뷰어로 변경을 리뷰하고 쉬운 말로 된 배포/수정 판정을 받습니다. 횟수 제한이 있는 수정 루프도 지원합니다 |
| [readme-writer](skills/readme-writer/README.md) | 저장소 근거를 바탕으로 README를 쓰고, 고치고, 번역합니다. 완성 예시와 템플릿이 들어 있습니다 |

각 스킬은 혼자서도 동작합니다. project-bootstrap은 git-hooks와 project-instructions가 설치되어 있으면 Git 훅과 에이전트 지침을 그쪽에 맡기고, 없으면 최소한만 직접 처리합니다.

## 지원 에이전트

스킬은 Agent Skills 형식(`SKILL.md`)이고 호스트 기능은 예로만 언급하므로, Agent Skills를 읽는 에이전트라면 어디서든 쓸 수 있습니다.

- **npm 설치기(이 패키지):** Codex, Claude Code
- **[Skills CLI](https://github.com/vercel-labs/skills):** Antigravity, Gemini CLI, GitHub Copilot, Cursor, Windsurf, OpenCode 등 이 도구가 지원하는 에이전트와 Codex, Claude Code

각 스킬의 eval 실행은 Claude Code에서 했습니다. 다른 에이전트는 형식상 지원하지만 여기서 시험하지는 않았습니다.

## 설치

Node.js 22.14 이상이 필요합니다. 모든 스킬을 두 호스트에 설치합니다.

```sh
npx @tortle1228/agent-skills@latest install --agent all
```

`--skill`로 스킬을 고르고(여러 번 쓸 수 있음), `--agent codex` 또는 `--agent claude-code`로 호스트를 고릅니다.

```sh
npx @tortle1228/agent-skills@latest install --agent claude-code --skill project-bootstrap --skill git-hooks
npx @tortle1228/agent-skills@latest list
```

설치기는 스킬을 `~/.agents/skills/<skill>`(Codex) 또는 `~/.claude/skills/<skill>`(Claude Code)로 복사하고 파일 해시를 기록합니다. 설치 후에는 npm 캐시에 의존하지 않고, `npm install`만으로는 실행되지 않습니다. 인자 없이 실행하면 도움말만 출력합니다.

다른 에이전트에 설치하거나 GitHub에서 바로 설치하려면 Skills CLI를 씁니다. 이 방법으로도 스킬 하나만 고를 수 있고, `-a` 값은 쓰는 에이전트로 바꾸면 됩니다.

```sh
npx skills add tortle1228/agent-skills --skill project-bootstrap -g -a codex -a claude-code
```

스킬과 호스트마다 한 가지 설치 방식만 쓰세요. 각 방식이 자기 설치본의 갱신과 제거를 맡습니다.

설치한 뒤에는 이름으로 부르거나(Codex는 `$project-bootstrap`, Claude Code는 `/project-bootstrap`) 할 일을 설명해서 호스트가 고르게 하면 됩니다. 새 스킬이 보이지 않으면 호스트를 다시 로드하거나 재시작하세요.

## 갱신과 제거

새 버전에서 설치 명령을 다시 실행하면 갱신됩니다. 직접 수정했거나, 이 설치기가 관리하지 않거나, 심볼릭 링크인 설치본은 충돌로 보고하고 건드리지 않습니다. 강제 옵션은 없습니다. 수정 내용을 백업하고 충돌하는 설치본을 옮긴 뒤 다시 시도하세요.

```sh
npx @tortle1228/agent-skills@latest uninstall --agent all --skill git-hooks
```

`--skill` 없이 실행하면 이 설치기가 관리하는 모든 스킬을 제거합니다. 다른 파일이나 이 저장소는 지우지 않습니다.

## 개발과 라이선스

[기여·릴리스 절차 — 영어](CONTRIBUTING.md)와 [변경 이력 — 영어](CHANGELOG.md)를 참고하세요. 스킬 동작은 각 스킬의 `evals/` 폴더에 있는 스킬 사용/미사용 비교 실행으로 확인합니다. 이 폴더는 패키지에 포함되지 않습니다.

직접 작성한 코드와 문서에는 [MIT 라이선스](LICENSE)가 적용됩니다. agent-code-review는 Ponytail의 자료를 MIT 라이선스에 따라 가져와 고쳤습니다. 해당 [NOTICE](skills/agent-code-review/NOTICE)를 참고하세요.
