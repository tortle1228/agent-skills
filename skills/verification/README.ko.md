# Verification

[English](README.md) | [한국어](README.ko.md)

에이전트가 작업이 끝났다고 말하기 전에 증거를 요구하는 에이전트 스킬입니다. 에이전트는 작업을 끝났다, 고쳤다, 통과한다고 주장하기 전에, 주장이 틀리면 실패할 검사를 직접 실행하고 결과를 읽은 뒤 그 증거와 함께 보고합니다.

## 하는 일

에이전트가 "끝났습니다", "고쳤습니다", "이제 동작합니다", "전부 green입니다"라고 말하려 할 때, 커밋·PR·인계 전, 그리고 서브에이전트의 성공 보고를 받았을 때 적용됩니다.

- **게이트:** 주장을 적고, 실패할 수 있는 증명을 고르고, 마지막 수정 뒤에 새로 실행하고, 출력 전체를 읽은 다음 보고합니다.
- **증거 표:** 주장 종류(테스트 통과, 버그 수정, 기능 동작, 위임 작업 완료)마다 무엇이 증거이고 무엇이 아닌지 정리합니다. 예를 들어 린트 통과는 빌드 성공의 증거가 아닙니다.
- **실제 표면:** CLI, 서비스, UI, 라이브러리 변경은 사용자가 닿는 경로로 직접 실행해 증명합니다. 문서·타입·테스트만 바꾼 변경은 `SKIP`입니다.
- **판정:** 주장마다 `PASS`, `FAIL`, `BLOCKED`, `SKIP` 중 하나로 보고하고, 확인하지 않은 것을 따로 적습니다. 실행하지 못한 검사는 통과로 보고하지 않습니다.

프로젝트에 `verify-*` 스킬이나 앱 실행 레시피가 있으면 그것을 씁니다. 없으면 `create-verification`을 한 번 제안할 수 있고, 없어도 동작합니다.

Codex에서는 `$verification`, Claude Code에서는 `/verification`으로 부르거나, 그냥 변경을 요청하면 에이전트가 보고하기 전에 자동으로 적용됩니다.

## 실행되는 것과 바뀌는 것

- 이 스킬은 에이전트가 보고하기 전에 검사를 하나 더 거치게 할 뿐입니다. 증거를 얻기 위해 에이전트가 프로젝트의 테스트, 빌드, 실행 명령을 돌립니다.
- 스스로 파일을 수정하거나 무언가를 설치하지 않습니다. 검증 중에 로컬 서버나 앱을 띄울 수 있으며, 띄운 것은 에이전트가 직접 종료해야 합니다.

## 설치

Node.js 22.14 이상이 필요합니다.

```sh
npx @tortle1228/agent-skills@latest install --agent all --skill verification
```

또는 별도의 Skills CLI로 GitHub에서 설치할 수 있습니다.

```sh
npx skills add tortle1228/agent-skills --skill verification -g -a codex -a claude-code
```

npm 설치기는 Codex와 Claude Code를 지원합니다. Antigravity, Gemini CLI, GitHub Copilot, Cursor, Windsurf, OpenCode처럼 Agent Skills(`SKILL.md`)를 읽는 다른 에이전트는 Skills CLI에 해당 에이전트 이름을 지정해 설치하세요. 예: `-a cursor`.

호스트마다 설치 방법은 하나만 고르세요. 설치된 사본은 `~/.agents/skills/verification`(Codex)과 `~/.claude/skills/verification`(Claude Code)에 있습니다.

## 업데이트와 제거

새 패키지 버전에서 설치 명령을 다시 실행하면 업데이트됩니다. 직접 수정한 설치본은 충돌로 보고하고 건드리지 않습니다.

```sh
npx @tortle1228/agent-skills@latest uninstall --agent all --skill verification
```

## 라이선스

[MIT](LICENSE).
