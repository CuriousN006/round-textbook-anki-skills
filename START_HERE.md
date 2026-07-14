# 저장소 링크 하나로 시작하기

이 문서는 이 저장소 URL을 처음 받은 일반 챗봇과 도구형 AI 에이전트가 공통으로 읽는 진입점입니다.

## 1. 먼저 현재 환경을 판별하세요

AI는 답변하기 전에 다음을 확인해야 합니다.

- 이 저장소의 파일을 실제로 열어 읽을 수 있는가?
- 사용자가 허용한 폴더에서 파일을 읽고 쓸 수 있는가?
- 로컬 명령을 실행할 수 있는가?
- MCP 또는 다른 커넥터를 통해 Anki 같은 외부 앱을 사용할 수 있는가?

하나라도 확인되지 않았다면 가능한 척하지 마세요. 일반 채팅 환경은 저장소를 설명하고 설치 절차를 안내할 수는 있지만, 사용자의 로컬 PDF를 읽거나 Anki Desktop에 카드를 저장할 수는 없습니다.

## 2. 일반 챗봇이라면 에이전트로 안내하세요

사용자에게 기술 지식을 요구하지 말고 다음 두 가지만 물어보세요.

1. Windows, macOS, Linux 중 어떤 운영체제를 사용하는가?
2. 화면에서 클릭하는 앱과 터미널 중 어느 방식이 더 편한가?

그 답에 맞춰 아래 선택지를 중립적으로 설명하고 최신 공식 설치 문서를 확인하세요. 저장소에 적힌 오래된 설치 명령을 현재의 절대적인 방법으로 단정하지 마세요.

- [Codex/ChatGPT 공식 시작 안내](https://learn.chatgpt.com/docs/quickstart): 데스크톱 앱, CLI, IDE에서 로컬 폴더를 열어 작업할 수 있습니다.
- [Google Antigravity 공식 시작 안내](https://antigravity.google/docs/editor): 프로젝트에 로컬 폴더 또는 Git 저장소를 연결해 에이전트를 실행할 수 있습니다.
- [Claude Code 공식 설치 안내](https://code.claude.com/docs/en/setup): 터미널과 지원 편집기에서 로컬 프로젝트를 다룰 수 있습니다.

특정 제품을 유일한 정답으로 단정하지 마세요. 계정 비밀번호, API 키, 액세스 토큰을 채팅에 붙여넣도록 요구하지 마세요. 로그인은 각 제품의 공식 로그인 화면이나 운영체제 보안 저장소를 사용하도록 안내하세요.

설치가 끝나면 새 에이전트에 저장소 URL과 아래 문장을 함께 전달하게 하세요.

```text
이 저장소를 읽고 START_HERE.md부터 따라가 줘.
내 환경을 먼저 읽기 전용으로 점검하고, 프로그램 설치·다운로드·설정 변경·Anki 쓰기는 실행 전에 설명하고 승인을 받아.
내가 알려 줘야 하는 정보는 기술 용어 대신 쉬운 말로 한 번에 하나씩 질문해 줘.
처음에는 2~3개 노트만 시험하고, 저장된 내용을 다시 읽어 확인한 뒤 전체 작업을 진행해 줘.
```

## 3. 이미 도구형 에이전트라면 바로 진단하세요

1. `README.md`와 `skills/round-textbook-anki/SKILL.md`를 읽습니다.
2. 원격에서 문서만 읽을 수 있다면 불필요하게 clone하지 않습니다. 로컬 스크립트 실행이나 PDF 접근이 필요할 때만 사용자의 작업 정책에 맞는 체크아웃 방법을 선택합니다.
3. 설치나 설정 변경 전에 아래 읽기 전용 진단을 실행합니다.

```powershell
python .\skills\round-textbook-anki\scripts\diagnose_environment.py
```

기계가 읽을 JSON이 필요하면 다음을 사용합니다.

```powershell
python .\skills\round-textbook-anki\scripts\diagnose_environment.py --json
```

이 진단은 파일이나 Anki 데이터를 수정하지 않습니다. 운영체제, Python과 필수 패키지, Node/`npx`, Anki 프로세스, 로컬 포트 `3141`·`8765`, AnkiConnect의 무해한 `version` 응답만 확인합니다.

## 4. 권한은 안전한 자동화로 설정하세요

권장 원칙은 다음과 같습니다.

- 저장소와 사용자가 지정한 PDF 폴더의 읽기, 저장소 안의 코드 수정, 정적 테스트는 작업 폴더 안에서 자동 진행할 수 있습니다.
- 프로그램 설치, 패키지 다운로드, 네트워크 접근, 작업 폴더 밖의 쓰기, MCP 설정 변경, Anki 노트 생성·수정·삭제는 실행 전에 이유와 범위를 설명하고 승인을 받습니다.
- 사용자가 원하면 제품의 자동 승인 검토 기능을 사용하되, 샌드박스나 위험 작업 차단을 끄는 방식은 권장하지 않습니다.
- 비밀번호·토큰 읽기, 보안 설정 완화, Anki 로컬 쓰기 포트의 인터넷 공개는 승인 여부와 관계없이 피합니다.

Codex에서는 공식 문서의 `Auto` 방식처럼 작업 폴더 쓰기와 필요 시 승인을 조합할 수 있습니다. 사용자가 반복 승인 대신 Codex가 위험도를 검토해 승인하기를 원하면 개인 설정에서 다음 조합을 검토할 수 있습니다.

```toml
approval_policy = "on-request"
approvals_reviewer = "auto_review"
```

이는 모든 권한을 무조건 허용하는 설정이 아닙니다. 위험도가 높은 작업은 여전히 거부되거나 사용자 승인이 필요할 수 있습니다. 자세한 내용은 [Codex 승인과 보안](https://learn.chatgpt.com/docs/agent-approvals-security)을 확인하세요.

Antigravity는 프로젝트 기본 경계와 `Ask`/`Allow` 규칙을 사용합니다. 안전하고 반복적인 읽기·테스트만 좁게 `Allow`하고, 설치·네트워크·MCP 쓰기는 `Ask`로 두세요. [Antigravity 권한 문서](https://antigravity.google/docs/permissions)를 확인하세요.

Claude Code는 기본 권한 확인을 유지하고, 반복되는 안전한 읽기·테스트 명령만 프로젝트 또는 개인 `allow` 규칙에 추가하세요. `--dangerously-skip-permissions`는 이 작업의 권장 설정이 아닙니다. [Claude Code 권한 문서](https://code.claude.com/docs/en/permissions)를 확인하세요.

## 5. 제품별 Skill과 MCP 경로를 선택하세요

제품별 자동 발견 위치와 설정 형식은 다릅니다. 자세한 비교와 공식 링크는 [`docs/agent-onboarding.md`](docs/agent-onboarding.md)를 읽으세요.

공통 원칙은 다음과 같습니다.

- `skills/round-textbook-anki/SKILL.md`, `references/`, `scripts/`가 재사용 가능한 핵심입니다.
- `skills/round-textbook-anki/agents/openai.yaml`은 Codex/ChatGPT용 메타데이터이며 다른 에이전트가 무시할 수 있습니다.
- Skill을 자동 발견 위치에 복사하는 작업은 설치에 해당하므로 먼저 승인받습니다. 자동 발견이 없어도 에이전트가 `SKILL.md`를 직접 읽고 현재 작업에 적용할 수 있습니다.
- Anki 연결은 [`docs/anki-mcp-setup.md`](docs/anki-mcp-setup.md)의 경로 중 현재 환경에 맞는 하나만 선택합니다.

## 6. 사용자에게 최소 정보만 요청하세요

다음 정보가 없을 때만 쉬운 말로 한 번에 하나씩 질문하세요.

1. PDF가 들어 있는 폴더
2. 만들고 싶은 상위 덱 이름
3. 전체 자료인지, 특정 교재·장·회차·문제 번호인지
4. Anki 프로필이나 미디어 폴더가 실제로 필요한 경우에만 해당 위치

승인 후 대화형 로컬 설정 도구를 사용할 수 있습니다.

```powershell
python .\skills\round-textbook-anki\scripts\configure_local_source.py
```

생성되는 `source-details.local.md`와 `source-manifest.local.json`은 Git에서 무시됩니다. 공개 커밋에 절대 경로, 저작권 PDF 내용, 개인 덱 정보가 들어가지 않았는지 확인하세요.

## 7. 소량 시험 후 저장 결과를 다시 읽으세요

1. 덱 목록처럼 무해한 읽기 작업으로 Anki 연결을 확인합니다.
2. 정확한 자료 범위와 정답 근거를 확인합니다.
3. 처음에는 2~3개 노트만 만듭니다.
4. 저장된 Front, Back, 덱, 태그, 이미지, 정답을 Anki에서 다시 읽습니다.
5. 문제가 없을 때만 전체 범위로 진행합니다.

실제 PDF나 Anki에 접근할 수 없다면 정적 검사와 모의 테스트만 수행하고, 실제 통합 검증을 했다고 주장하지 마세요.
