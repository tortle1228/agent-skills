# Work Tracking

[English](README.md) | [한국어](README.ko.md)

저장소의 계획된 작업과 결정을 어디에 둘지 한 번 정하고, 그 규칙을 몇 줄로 기록하는 에이전트 스킬입니다. 에이전트가 로드맵, ADR, 조사 문서를 알아서 만들고 동기화하는 일을 막습니다.

## 하는 일

저장소를 살펴본 뒤 질문을 하나씩 하고, 신호에 맞는 답을 추천합니다.

| 선택 | 계획된 작업을 두는 곳 | 쓰는 섹션 |
| --- | --- | --- |
| GitHub Issues | `gh`로 다루는 이슈와 `roadmap`, `backlog`, `when-needed` 라벨 | [issues](assets/section-issues.md) |
| 단일 파일 | `ROADMAP.md` 한 파일, 항목당 한 줄 | [roadmap](assets/section-roadmap.md) |
| 추적 문서 없음 | 코드 주석과 커밋 본문, `Decision:` trailer | [commits](assets/section-commits.md) |

선택한 방식을 어디에 기록할지도 묻습니다. `AGENTS.md`의 짧은 "Work tracking" 섹션(추천) 또는 별도 `docs/agents/work-tracking.md`입니다. 초안을 보여 주고 확인한 뒤에만 씁니다.

모든 섹션에는 같은 규모 규칙이 들어갑니다. 발견은 한 곳에만 기록하고, 지침 파일에는 명령과 함정만 두며, ADR이나 조사 문서는 요청이 있을 때만 만듭니다.

Codex에서는 `$work-tracking`, Claude Code에서는 `/work-tracking`으로 부르거나 할 일만 설명해도 됩니다.

## 실행하는 것과 바뀌는 것

- 점검은 읽기 전용입니다. `git remote -v`, `gh repo view`, `gh issue list`를 실행하고 `ROADMAP.md`, `docs/`, 기존 "Work tracking" 섹션을 찾습니다. 기존 섹션은 덮어쓰지 않습니다.
- 라벨은 확인을 받은 뒤에만 `gh label create`로 만듭니다. 이슈는 만들지 않습니다.
- 쓰는 파일은 해당 섹션(또는 고른 파일 하나)뿐입니다.

## 설치

Node.js 22.14 이상이 필요합니다.

```sh
npx @tortle1228/agent-skills@latest install --agent all --skill work-tracking
```

별도 Skills CLI로 GitHub에서 설치할 수도 있습니다.

```sh
npx skills add tortle1228/agent-skills --skill work-tracking -g -a codex -a claude-code
```

제거는 `npx @tortle1228/agent-skills@latest uninstall --agent all --skill work-tracking`입니다.

## 라이선스

[MIT](LICENSE).
