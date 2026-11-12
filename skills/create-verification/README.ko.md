# Create Verification

[English](README.md) | [한국어](README.ko.md)

저장소를 읽고 프로젝트 로컬 `verify-<app>` 스킬을 만드는 에이전트 스킬입니다. 실제 앱을 띄우고, 사용자처럼 조작하고, 증거를 남기는 레시피입니다. 생성한 스킬은 넘기기 전에 한 번 직접 실행해 증명합니다.

## 하는 일

UI, CLI, 서비스의 동작을 증명할 스크립트화된 방법이 없는 저장소에서 요청하면 됩니다. 예를 들면:

> 이 저장소용 검증 스킬을 만들어 주세요. 에이전트가 실제로 실행해서 동작하는 걸 보여 줄 수 있게요.

사용자가 무엇을 만지는지, 앱을 어떻게 시작하는지, 어떻게 조작하고 관찰하는지, 인스턴스 두 개를 나란히 띄울 수 있는지는 코드에서 직접 알아내고, 보이지 않는 것만 묻습니다. 그런 다음 다음을 만듭니다.

- `verify-<app>/SKILL.md`: **Launch**, **Doctor**, **Drive**, **Evidence**, **Cleanup**과 보조 스크립트. 이 저장소의 실제 명령과 셀렉터를 씁니다.
- `verify-<app>/features/`: 인덱스와 사용자에게 보이는 주요 기능 3~5개의 파일. 형태는 [템플릿](references/verify-skill-template.md)에 있습니다.

이어서 자기가 만든 레시피를 한 번 따라 합니다. 실행, doctor, 기능 하나 조작, 증거 수집, 정리, 그리고 증거가 남아 있는지 확인까지 합니다. 저장소의 임시 복사본에서 동작 하나를 일부러 깨뜨려 검사가 실패함도 보입니다. 앱이 빌드되거나 시작되지 않으면 임시 레시피를 쓰는 대신 이유를 정확히 보고합니다. 대체 환경에서 증명했다면 실제 대상에서 아직 필요한 단계를 목록으로 남깁니다.

Codex에서는 `$create-verification`, Claude Code에서는 `/create-verification`으로 부릅니다. 생성된 레시피를 쓰는 `verification` 스킬과 짝이지만 각각 혼자서도 동작합니다.

## 실행되는 것과 바뀌는 것

- 에이전트는 프로젝트 로컬 스킬 폴더 안의 새 `verify-<app>/` 폴더에만 파일을 씁니다. 작업 트리의 제품 코드는 수정하지 않습니다.
- 검사가 실패할 수 있음을 보이려고 저장소의 임시 복사본에서 동작 하나를 깨뜨렸다가, 끝나면 복사본을 버립니다.
- 레시피를 증명하려고 앱을 로컬에서 빌드하고 시작하고, 기능 하나를 조작한 뒤 직접 띄운 것을 종료합니다. 관련 없는 파일이 없어 시작이 막히면 검증용임을 표시한 임시 파일을 만들었다가 나중에 지웁니다.
- 증거 파일은 정리 후에도 생성된 스킬이 지정한 위치에 남습니다.

## 설치

Node.js 22.14 이상이 필요합니다.

```sh
npx @tortle1228/agent-skills@latest install --agent all --skill create-verification
```

또는 별도의 Skills CLI로 GitHub에서 설치할 수 있습니다.

```sh
npx skills add tortle1228/agent-skills --skill create-verification -g -a codex -a claude-code
```

npm 설치기는 Codex와 Claude Code를 지원합니다. Antigravity, Gemini CLI, GitHub Copilot, Cursor, Windsurf, OpenCode처럼 Agent Skills(`SKILL.md`)를 읽는 다른 에이전트는 Skills CLI에 해당 에이전트 이름을 지정해 설치하세요. 예: `-a cursor`.

호스트마다 설치 방법은 하나만 고르세요. 설치된 사본은 `~/.agents/skills/create-verification`(Codex)과 `~/.claude/skills/create-verification`(Claude Code)에 있습니다.

## 업데이트와 제거

새 패키지 버전에서 설치 명령을 다시 실행하면 업데이트됩니다. 직접 수정한 설치본은 충돌로 보고하고 건드리지 않습니다. 스킬을 제거해도 이미 저장소에 만들어 둔 `verify-<app>` 스킬은 지워지지 않습니다.

```sh
npx @tortle1228/agent-skills@latest uninstall --agent all --skill create-verification
```

## 라이선스

[MIT](LICENSE).
