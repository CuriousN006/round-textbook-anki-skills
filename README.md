# 교재·문제은행 Anki 카드 제작용 Codex Skill

이 저장소는 교재, 문제집, 문제은행, 모의고사, 기출문제, 면접 대비 자료, 개념 PDF 같은 학습 자료를 검토 가능한 Anki 노트로 바꾸기 위한 공개 Codex Skill을 제공합니다.

저작권과 개인정보 보호를 위해 이 저장소에는 PDF 원본, 렌더링한 페이지 이미지, Anki 내보내기 파일, 컬렉션 미디어, 정답지, 로컬 컴퓨터 경로를 넣지 않습니다. 실제 자료 경로, 덱 이름, 개인별 작업 메모는 Git에서 무시되는 `source-details.local.md`에만 보관하세요.

## 이 저장소를 처음 보는 분을 위한 기본 개념

### 간격 반복 학습이란?

간격 반복 학습(spaced repetition)은 한 번 공부한 내용을 잊어버리기 직전에 다시 복습하도록 복습 간격을 점점 늘려 가는 학습 방법입니다. 사람은 시간이 지나면 자연스럽게 내용을 잊어버리지만, 적절한 시점에 다시 떠올리면 기억이 더 오래 유지됩니다. 그래서 매일 모든 카드를 반복해서 보는 대신, 쉬운 카드는 며칠 또는 몇 주 뒤로 미루고 어려운 카드는 더 빨리 다시 보게 합니다.

이 방식은 단순 암기뿐 아니라 다음과 같은 작업에도 잘 맞습니다.

- 공식, 정의, 용어, 판례, 문법, 어휘처럼 정확히 떠올려야 하는 내용
- 문제 풀이 절차, 함정, 오답 포인트처럼 반복 훈련이 필요한 내용
- 시험 범위가 넓어서 모든 내용을 매일 다시 보기 어려운 장기 학습

### Anki란?

Anki는 간격 반복 학습을 자동으로 관리해 주는 플래시카드 프로그램입니다. 사용자는 앞면(front)에 질문, 문제, 단서, 이미지 등을 넣고 뒷면(back)에 정답, 해설, 근거, 풀이 과정을 넣습니다. Anki는 사용자가 각 카드를 얼마나 쉽게 맞혔는지에 따라 다음 복습 날짜를 자동으로 정합니다.

이 저장소의 Skill은 PDF 자료에서 문제와 해설을 정리해 Anki에 넣기 좋은 형태의 노트를 만드는 절차를 돕습니다. 특히 번호가 반복되는 회차별 문제, 장별 문제, 기출 회차, 모의고사 묶음처럼 사람이 헷갈리기 쉬운 자료를 다룰 때 검증 절차를 강조합니다.

### Anki는 PC와 모바일에서 어떻게 쓰나?

Anki는 보통 PC에서 카드를 만들고 정리한 뒤, 모바일에서는 짧은 시간에 복습하는 방식으로 함께 사용합니다. PC용 Anki Desktop은 카드 편집, 이미지 확인, 대량 수정, 애드온 설치, MCP/AnkiConnect 연결 같은 관리 작업에 적합합니다. 모바일 앱은 이동 중 복습, 시험 직전 확인, 매일 정해진 복습량 처리에 적합합니다.

플랫폼별로는 일반적으로 다음처럼 이해하면 됩니다.

- **PC**: Windows, macOS, Linux에서 Anki Desktop을 사용합니다. 이 저장소의 Codex Skill과 MCP/AnkiConnect 연동은 기본적으로 PC에서 열린 Anki Desktop을 대상으로 합니다.
- **iPhone/iPad**: 공식 iOS 앱인 AnkiMobile을 사용해 AnkiWeb과 동기화한 덱을 복습할 수 있습니다.
- **Android**: AnkiDroid를 사용해 AnkiWeb과 동기화한 덱을 복습할 수 있습니다.
- **웹**: AnkiWeb은 동기화와 간단한 복습에 유용하지만, 대량 카드 편집이나 로컬 MCP 연동의 중심은 보통 Anki Desktop입니다.

### Anki 동기화는 어떻게 생각해야 하나?

Anki 동기화는 PC, 모바일, 웹에 흩어진 같은 덱을 AnkiWeb 계정 기준으로 맞추는 과정입니다. 예를 들어 PC에서 Codex가 새 카드를 만든 뒤 Anki Desktop에서 동기화하면, 모바일 앱에서도 같은 카드를 내려받아 복습할 수 있습니다. 반대로 모바일에서 복습한 결과를 동기화하면 PC에서도 다음 복습 일정이 반영됩니다.

권장 흐름은 다음과 같습니다.

1. PC의 Anki Desktop에서 덱을 만들거나 Codex/MCP로 노트를 추가합니다.
2. Anki Desktop에서 동기화를 실행해 AnkiWeb에 업로드합니다.
3. 모바일 앱에서 같은 AnkiWeb 계정으로 동기화해 새 카드와 미디어를 내려받습니다.
4. 모바일에서 복습한 뒤 다시 동기화합니다.
5. PC로 돌아오면 Anki Desktop도 먼저 동기화한 뒤 추가 편집을 합니다.

동기화할 때는 한 기기에서 대량 수정 중인 상태로 다른 기기에서도 동시에 편집하지 않는 편이 안전합니다. 이미지가 포함된 카드나 새로 만든 카드가 모바일에 보이지 않는다면, PC와 모바일 양쪽에서 동기화를 다시 실행하고 미디어 동기화가 끝났는지 확인하세요.

### Codex란?

Codex는 OpenAI의 코딩 및 작업 자동화 에이전트입니다. 이 저장소에서는 Codex가 사용자의 로컬 자료를 살펴보고, 문제를 카드로 나누고, OCR 결과를 정리하고, 이미지 크롭을 만들고, Anki에 저장된 노트를 다시 확인하는 작업을 일관된 절차로 수행하도록 지침을 제공합니다.

중요한 점은 Codex가 이 저장소만으로 사용자의 Anki 앱이나 로컬 PDF에 자동 접근할 수 있는 것은 아니라는 점입니다. 실제 PDF 경로와 Anki 연결 설정은 사용자의 컴퓨터에서 별도로 구성해야 합니다.

### MCP란?

MCP(Model Context Protocol)는 AI 도구가 외부 프로그램이나 로컬 서비스와 안전하고 표준화된 방식으로 통신하기 위한 프로토콜입니다. 이 저장소의 맥락에서는 Codex가 Anki Desktop에 직접 접근하는 대신, MCP 서버나 AnkiConnect 같은 로컬 브리지를 통해 덱 목록을 읽고 노트를 만들거나 검증할 수 있게 합니다.

예를 들어 다음과 같은 구조가 가능합니다.

```text
Codex 또는 MCP 호스트 → Anki MCP 서버 또는 AnkiConnect 래퍼 → Anki Desktop
```

Anki 연결 설정은 환경마다 다르므로 자세한 내용은 [`docs/anki-mcp-setup.md`](docs/anki-mcp-setup.md)를 참고하세요.

### Skills란?

Skills는 Codex가 특정 작업을 더 안정적으로 수행하도록 만드는 작업 지침 묶음입니다. 이 저장소의 `round-textbook-anki` Skill은 “여러 PDF 학습 자료를 확인하고, 문제를 정확히 식별하고, Anki 카드로 만들고, 저장 후 다시 검증하라”는 절차를 담고 있습니다.

일반 프롬프트만으로도 카드를 만들 수는 있지만, Skill을 사용하면 다음과 같은 장점이 있습니다.

- 자료 목록 확인, 출처 검증, 카드 작성, 저장 후 검토의 순서가 명확해집니다.
- 문제 번호가 회차나 장마다 다시 시작되는 자료에서도 식별 실수를 줄입니다.
- 정답지와 저장된 Anki 노트를 다시 확인하는 품질 점검 단계를 빠뜨리지 않습니다.
- 개인 자료 경로와 공개 저장소에 올리면 안 되는 파일을 분리하도록 안내합니다.

## 이 Skill이 다루는 작업

- 소스 폴더를 조사하고 PDF 종류를 분류한 뒤 덱 구조를 정합니다.
- 요청된 교재, 회차, 시험, 장, 주제, 기관 시험, 문제 묶음을 실제 페이지에서 먼저 확인합니다.
- 회차, 장, 시험 세션마다 문제 번호가 `01`부터 다시 시작되는 경우에도 독립 번호 체계를 구분합니다.
- OCR 정리, MathJax, 이미지 크롭, 정답 확인, 새로 작성한 해설을 포함해 학습하기 좋은 Anki 앞면과 뒷면을 만듭니다.
- 노트 생성 후 MCP 또는 AnkiConnect로 저장된 Anki 노트를 다시 읽어 실제 컬렉션 상태를 기준으로 최종 보고합니다.
- 작업 완료를 선언하기 전에 저장된 정답을 해당 정답표나 해설 부분과 대조합니다.

## 저장소 구조

```text
skills/
  round-textbook-anki/
    SKILL.md
    agents/openai.yaml
    references/
      card-patterns.md
      crop-workflow.md
      quality-audit.md
      source-taxonomy.md
      source-details-template.md
    scripts/
      crop_problem_images.py
      inventory_pdf_sources.py
```

## 로컬 설치 방법

이 저장소의 루트에서 다음 명령을 실행합니다.

```powershell
Copy-Item -Recurse -Force .\skills\round-textbook-anki "$env:USERPROFILE\.codex\skills\round-textbook-anki"
```

그다음 Codex 세션을 새로 시작해 Skill 목록을 갱신합니다. 학습 자료 폴더, 교재, 장, 회차, 시험지, 번호가 붙은 문제 묶음으로 작업할 때 프롬프트에서 `$round-textbook-anki`를 요청하세요.

## Anki MCP 설정

이 Skill은 카드 생성과 검증 절차를 계획할 수 있지만, Codex가 실제 Anki 컬렉션을 읽거나 수정하려면 로컬 Anki 브리지가 필요합니다.

[`docs/anki-mcp-setup.md`](docs/anki-mcp-setup.md)는 “Codex가 내 PC의 Anki Desktop에 어떻게 연결되는가?”를 설명하는 로컬 연결 설정 문서입니다. 모바일 동기화 설명서가 아니라, Anki Desktop과 Codex/MCP 사이에 필요한 브리지 선택지, 포트, 설정 예시, 연결 확인, 문제 해결을 정리한 문서입니다.

자세한 설정은 [`docs/anki-mcp-setup.md`](docs/anki-mcp-setup.md)를 읽어 보세요. 해당 문서에는 다음 내용이 포함되어 있습니다.

- 로컬 Codex에서 흔히 `http://127.0.0.1:3141`을 사용하는 네이티브 AnkiMCP 애드온 설정
- 흔히 `http://127.0.0.1:8765`을 사용하는 AnkiConnect와 MCP 래퍼 설정
- Codex/MCP 설정 예시
- PowerShell 연결 확인 명령
- `502`, `connection refused`, 오래된 도구 목록, 포트 또는 변형 혼동 문제 해결

## 개인 소스 설정

다음 템플릿 파일을 복사합니다.

```text
skills/round-textbook-anki/references/source-details-template.md
```

그리고 아래 위치에 로컬 전용 파일을 만듭니다.

```text
skills/round-textbook-anki/references/source-details.local.md
```

이 파일에는 로컬 파일 경로, 덱 이름, 미디어 디렉터리, 자료별 주의사항을 적습니다. 이 파일은 커밋하지 마세요.

첫 번째 로컬 매니페스트를 만들려면 다음 명령을 사용할 수 있습니다.

```powershell
python .\skills\round-textbook-anki\scripts\inventory_pdf_sources.py `
  --root "C:\path\to\study-pdfs" `
  --output ".\source-manifest.local.json"
```

Anki 노트를 만들기 전에 생성된 매니페스트를 검토하고 필요하면 직접 수정하세요.

## 공개 저장소 안전 규칙

- 저작권이 있는 PDF, 렌더링한 페이지, 이미지 크롭, 정답 목록, 교재 문단 복사본을 커밋하지 않습니다.
- 절대 경로, Anki 프로필 경로, API 토큰, 개인 덱 내보내기 파일을 커밋하지 않습니다.
- 해설지는 정답과 풀이 방향을 확인하는 참고 자료로만 사용하고, Anki 카드의 설명은 새로 작성한 교육용 문장으로 정리합니다.

## 권장 작업 흐름

1. 로컬 PDF 자료 폴더를 준비합니다.
2. `source-details.local.md`에 개인 경로와 덱 이름을 기록합니다.
3. `inventory_pdf_sources.py`로 자료 목록을 만들고 사람이 한 번 검토합니다.
4. Codex에 `$round-textbook-anki` Skill 사용을 요청하면서 작업 범위, 회차, 장, 문제 번호를 명확히 지정합니다.
5. Codex가 원문 페이지와 정답 근거를 확인한 뒤 Anki 카드 초안을 만듭니다.
6. MCP 또는 AnkiConnect 연결을 통해 PC의 Anki Desktop에 실제 노트를 저장합니다.
7. 저장된 노트를 다시 읽어 정답, 태그, 덱, 이미지, 해설이 의도대로 들어갔는지 확인합니다.
8. Anki Desktop에서 AnkiWeb으로 동기화한 뒤 모바일 앱에서도 동기화해 복습합니다.

## 한 줄 요약

이 저장소는 여러 종류의 학습 PDF를 안전하게 다루면서, 문제와 해설을 검증 가능한 Anki 카드로 바꾸기 위한 Codex Skill입니다.
