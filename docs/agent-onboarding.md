# 에이전트별 설치·Skill·권한 안내

이 문서는 일반 챗봇이 사용자를 도구형 에이전트로 안내하거나, 이미 설치된 에이전트가 이 저장소를 자기 환경에 연결할 때 참고하는 제품별 차이입니다. 제품 인터페이스와 설치 방법은 바뀔 수 있으므로 실행 전 공식 문서를 다시 확인하세요.

## 공통 선택 기준

- GUI가 편하면 로컬 폴더를 프로젝트로 여는 데스크톱 앱을 우선 고려합니다.
- 터미널이 편하면 운영체제를 공식 지원하는 CLI를 고려합니다.
- 어떤 제품이든 파일 읽기·쓰기와 명령 실행 권한이 실제로 있는지 확인합니다.
- 원격 웹 세션만으로 사용자의 PC나 Anki에 접근할 수 있다고 가정하지 않습니다.
- 설치·다운로드·설정 변경은 사용자에게 설명하고 승인받은 뒤 실행합니다.

## Codex/ChatGPT

- 공식 시작 문서: <https://learn.chatgpt.com/docs/quickstart>
- 승인과 보안: <https://learn.chatgpt.com/docs/agent-approvals-security>
- Skill 작성·발견: <https://learn.chatgpt.com/docs/build-skills>
- MCP 설정: <https://learn.chatgpt.com/docs/extend/mcp>

Codex는 저장소 또는 사용자 범위의 `.agents/skills/<skill-name>/SKILL.md`를 발견할 수 있습니다. 이 저장소의 Skill을 자동 발견 위치에 설치하지 않아도, 현재 세션에서 `skills/round-textbook-anki/SKILL.md`를 직접 읽고 따를 수 있습니다.

권장 권한은 작업 폴더 안 읽기·쓰기와 명령 실행을 허용하고, 네트워크·작업 폴더 밖 쓰기·설정 변경은 필요할 때 승인하는 `Auto` 계열입니다. 반복 승인 부담을 줄이려면 샌드박스를 끄는 대신 `approvals_reviewer = "auto_review"`를 검토하세요.

## Google Antigravity

- 공식 시작 문서: <https://antigravity.google/docs/editor>
- Agent Skills: <https://antigravity.google/docs/skills>
- MCP: <https://antigravity.google/docs/mcp>
- 권한: <https://antigravity.google/docs/permissions>

Antigravity는 프로젝트의 `.agents/skills/<skill-name>/SKILL.md` 또는 사용자 범위의 `~/.gemini/config/skills/<skill-name>/SKILL.md`를 발견합니다. 제품 버전에 따라 UI와 자동 발견 경로가 달라질 수 있으므로 공식 문서를 우선합니다.

프로젝트에 이 저장소와 로컬 PDF 폴더를 필요한 범위만 연결하세요. 작업 폴더 읽기·쓰기는 기본 프로젝트 경계 안에서 진행하고, 터미널 명령과 MCP는 처음에는 `Ask`를 유지하세요. 반복되는 안전한 읽기·테스트 작업만 구체적인 범위로 `Allow`할 수 있습니다.

## Claude Code

- 공식 설치 문서: <https://code.claude.com/docs/en/setup>
- Skills: <https://code.claude.com/docs/en/skills>
- MCP: <https://code.claude.com/docs/en/mcp>
- 권한: <https://code.claude.com/docs/en/permissions>

Claude Code는 프로젝트의 `.claude/skills/<skill-name>/SKILL.md` 또는 사용자 범위의 `~/.claude/skills/<skill-name>/SKILL.md`를 발견합니다. 이 저장소의 공통 Skill을 해당 위치로 복사하거나, 현재 세션에서 직접 읽어 적용할 수 있습니다.

기본 권한 확인을 유지하고 안전한 읽기·테스트 명령만 `permissions.allow`에 좁게 추가하세요. 설정은 개인용 `~/.claude/settings.json`, 공유 프로젝트용 `.claude/settings.json`, Git에서 제외되는 로컬용 `.claude/settings.local.json`처럼 범위가 다릅니다. 전체 권한 확인을 건너뛰는 옵션은 사용하지 마세요.

## 호환성 경계

이 저장소는 Codex 흐름을 중심으로 검증했습니다. Antigravity와 Claude Code는 공통 Agent Skills 형식과 MCP를 지원하지만 이 저장소의 실제 Anki 통합 시험은 아직 수행하지 않았습니다. 따라서 다음을 따르세요.

- 공통 `SKILL.md`, 참고 문서, Python 스크립트를 재사용합니다.
- 제품 전용 메타데이터가 다른 제품에서도 작동한다고 가정하지 않습니다.
- 해당 제품의 Skill 자동 발견과 MCP 설정을 공식 문서로 확인합니다.
- 정적 또는 모의 테스트 결과와 실제 Anki 통합 결과를 구분해 보고합니다.
