# Agent Code Review

[English](README.md) | [한국어](README.ko.md)

장애가 나면 호출받는 시니어 개발자처럼 코드 변경을 리뷰하고, 쉬운 말로 "배포 가능/수정 필요" 판정을 내려 주는 에이전트 스킬입니다.

## 하는 일

| 모드 | 요청 예시 | 결과 |
| --- | --- | --- |
| 리뷰만 | "커밋 전 변경사항 리뷰해 주세요." / "마지막 커밋 리뷰해 주세요." | 꼭 고칠 것, 고치면 좋은 것, 선택 사항으로 나눈 지적. 항목마다 구체적인 실패 사례와 가장 작은 수정안이 붙습니다. 코드는 바꾸지 않습니다 |
| 수정 루프 | "리뷰하고 필요한 건 고쳐 주세요." / 에이전트가 여러 파일 작업을 끝냈다고 말하기 전 | 분리된 리뷰어, 검증된 지적, 수정, 재확인을 최대 3라운드 진행한 뒤 같은 형식의 보고서와 고친 것·기각한 것 |

애매하면 리뷰만 모드를 씁니다. 요청하지 않은 코드 변경은 질문 한 번보다 되돌리기 어렵기 때문입니다.

리뷰를 쓸모 있게 유지하는 방법:

- 프로젝트의 빌드, 타입 검사, 린트, 테스트를 먼저 돌려서, 기계가 잡을 수 없는 부분에 리뷰를 집중합니다.
- 리뷰는 새 컨텍스트(호스트가 지원하면 서브에이전트)에서 작성자의 요약이 아니라 원래 요청을 보고 진행합니다. 서브에이전트가 없으면 보고서에 그렇게 적습니다.
- 지적에는 "이 입력이면 이런 잘못된 결과가 나온다"는 구체적인 사례가 있어야 합니다. 막연한 걱정과 취향 문제는 버리고, 틀린 지적은 이유를 붙여 기각합니다.
- 루프는 최대 3라운드입니다. 요구사항이 애매하거나 아키텍처 선택이 필요하면 사용자에게 넘깁니다.
- 보고서는 라벨까지 전부 사용자의 언어로, 코드를 처음 보는 사람도 읽을 수 있게 짧은 문장으로 씁니다. [보고서 형식(영어)](references/report-format.md)을 참고하세요.

Codex에서는 `$agent-code-review`, Claude Code에서는 `/agent-code-review`로 부르거나 평소 말로 리뷰를 요청하면 됩니다.

## 실행하는 것과 바꾸는 것

번들 스크립트는 없습니다. 에이전트는 프로젝트에 이미 있는 명령(패키지 스크립트, Makefile, CI 설정, README)을 실행합니다. 리뷰만 모드에서는 파일을 바꾸지 않습니다. 수정 루프 모드에서는 받아들인 수정에 필요한 파일만 고치고, 라운드마다 테스트를 다시 돌립니다. 요청하지 않으면 커밋하지 않습니다.

## 설치

Node.js 22.14 이상이 필요합니다.

```sh
npx @tortle1228/agent-skills@latest install --agent all --skill agent-code-review
```

별도 Skills CLI로 GitHub에서 설치할 수도 있습니다.

```sh
npx skills add tortle1228/agent-skills --skill agent-code-review -g -a codex -a claude-code
```

npm 설치기는 Codex와 Claude Code를 지원합니다. Antigravity, Gemini CLI, GitHub Copilot, Cursor, Windsurf, OpenCode처럼 Agent Skills(`SKILL.md`)를 읽는 다른 에이전트에는 Skills CLI에 해당 에이전트 이름을 붙여 설치합니다(예: `-a cursor`).

호스트마다 한 가지 설치 방식만 쓰세요. 설치본은 `~/.agents/skills/agent-code-review`(Codex)와 `~/.claude/skills/agent-code-review`(Claude Code)에 있습니다.

## 갱신과 제거

새 버전 패키지로 설치 명령을 다시 실행하면 갱신됩니다. 직접 수정한 설치본은 충돌로 보고하고 건드리지 않습니다.

```sh
npx @tortle1228/agent-skills@latest uninstall --agent all --skill agent-code-review
```

## 라이선스

[MIT](LICENSE). 리뷰 순서, 지적 검증 방식, 보고서 형식은 Ponytail의 ponytail-review 스킬을 MIT 라이선스에 따라 가져와 고친 것입니다. [NOTICE](NOTICE)를 참고하세요.
