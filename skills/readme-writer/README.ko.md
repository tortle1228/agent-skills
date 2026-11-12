# README Writer

[English](README.md) | [한국어](README.ko.md)

저장소의 실제 근거를 바탕으로 README를 작성·개선합니다. 에이전트 스킬, 7종 완성 예시와 템플릿, 사람과 에이전트를 위한 지침을 제공합니다.

상세 지침과 해설은 **영어**입니다. 이 홈과 앱 예시에는 한국어판도 있습니다. 문서를 읽기 위해 설치할 필요는 없습니다.

## 스킬 설치

Node.js 22.14 이상이 필요합니다. 이 스킬은 `@tortle1228/agent-skills` 패키지에 들어 있습니다. 이 스킬만 두 도구에 설치하거나 `all` 대신 `codex` 또는 `claude-code`를 선택합니다.

```sh
npx @tortle1228/agent-skills@latest install --agent all --skill readme-writer
```

Codex에서는 `$readme-writer`, Claude Code에서는 `/readme-writer`로 호출합니다. 신규 작성·부분 수정·번역 중 원하는 작업과 출력 언어를 지정하세요. 지원 호스트는 스킬을 자동 발견하며, 보이지 않으면 다시 로드하거나 재시작합니다.

설치본은 Codex의 `~/.agents/skills/readme-writer`, Claude Code의 `~/.claude/skills/readme-writer`에 복사됩니다. 이후 npm 캐시에 의존하지 않으며 `npm install`만으로 실행되지 않습니다.

새 버전에서 같은 명령을 실행하면 갱신합니다. `latest` 대신 버전을 지정해 고정할 수 있습니다. 수정된 파일·타 도구의 설치본·심볼릭 링크는 변경하지 않고 충돌을 보고합니다. 수정 내용을 백업하고 충돌하는 설치본을 직접 옮기거나 제거한 뒤 다시 시도하세요. 강제 덮어쓰기는 지원하지 않습니다.

```sh
npx @tortle1228/agent-skills@latest uninstall --agent all --skill readme-writer
```

이 설치기가 관리하는 수정되지 않은 설치본만 제거합니다. 원본 저장소는 지우지 않습니다. 인자 없이 실행하면 도움말만 표시합니다.

별도 Skills CLI로 GitHub에서 설치할 수도 있습니다.

```sh
npx skills add tortle1228/agent-skills --skill readme-writer -g -a codex -a claude-code
```

npm 설치기는 Codex와 Claude Code를 지원합니다. Antigravity, Gemini CLI, GitHub Copilot, Cursor, Windsurf, OpenCode처럼 Agent Skills(`SKILL.md`)를 읽는 다른 에이전트에는 Skills CLI에 해당 에이전트 이름을 붙여 설치합니다(예: `-a cursor`).

호스트별로 한 가지 설치 방식을 선택하세요. Skills CLI로 설치한 경우 해당 도구로 갱신·제거하며, 이 패키지는 그 설치본을 덮어쓰지 않습니다.

## 읽고 적용하기

1. [작성 원칙 — 영어](guides/writing.md)을 읽습니다.
2. 유형에 맞는 예시와 해설을 비교합니다.
3. 템플릿을 실제 프로젝트 사실로 채우고 불필요한 섹션은 뺍니다.
4. [검토 기준 — 영어](guides/maintenance.md)을 확인합니다.

| 유형 | 예시 (영어) | 해설 (영어) | 템플릿 (영어) |
| --- | --- | --- | --- |
| Swift 패키지 | [예시](examples/swift-package/README.md) | [해설](examples/swift-package/EXPLAIN.md) | [템플릿](templates/swift-package.md) |
| CLI | [예시](examples/cli/README.md) | [해설](examples/cli/EXPLAIN.md) | [템플릿](templates/cli.md) |
| 화면 중심 앱 | [예시](examples/app/README.md) | [해설](examples/app/EXPLAIN.md) | [템플릿](templates/app.md) |
| MCP 서버 | [예시](examples/mcp-server/README.md) | [해설](examples/mcp-server/EXPLAIN.md) | [템플릿](templates/mcp-server.md) |
| 코딩 에이전트 | [예시](examples/coding-agent/README.md) | [해설](examples/coding-agent/EXPLAIN.md) | [템플릿](templates/coding-agent.md) |
| 스킬 패키지 | [예시](examples/skill-package/README.md) | [해설](examples/skill-package/EXPLAIN.md) | [템플릿](templates/skill-package.md) |
| pi 확장·패키지 | [예시](examples/pi-package/README.md) | [해설](examples/pi-package/EXPLAIN.md) | [템플릿](templates/pi-package.md) |

## 지침 — 영어

- [작성 원칙](guides/writing.md)
- [이미지·언어·문서 연결](guides/github-formatting.md)
- [배포 패키지](guides/distribution.md)
- [AI 작성](guides/ai-writing.md)
- [유지관리](guides/maintenance.md)
- [라이선스 안내](guides/licensing.md)

[조사 기록 — 영어](references/README.md)은 유명 저장소·조회일을 기록한 Trending 20개·에이전트·스킬·pi 패키지·Awesome README를 다룹니다. 제품 감사나 품질 순위가 아닙니다.

## 개발과 라이선스

기여·릴리스 절차와 변경 이력은 `@tortle1228/agent-skills` 저장소에 있습니다. 예시는 가상 문서이며 해당 제품의 구현은 포함하지 않습니다. README Writer는 작성 스킬이며 README 생성 서비스나 호스팅 사이트가 아닙니다.

직접 작성한 코드·문서·템플릿·목업에는 [MIT 라이선스](LICENSE)가 적용됩니다. 외부 참고 자료는 각자의 이용 조건을 따릅니다.
