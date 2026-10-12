# AI 투자 브레인 기획안 리뷰 — Claude Fable

- 리뷰 모델: claude-fable-5-1 (`claude -p`)
- 리뷰 일시: 2026-10-12
- 대상: `~/workspace/goals/50/guru-brain/` 기획 문서 전체 (README, ARCHITECTURE, USAGE, PORTABLE, OBSIDIAN-MCP-SETUP, GURU_TEMPLATE, books/_index, gurus/_index, synthesis 3종, 농구천재 노트 10건)
- 관점: 아키텍처 타당성, 빠진 부분, 옵시디언 호환성, 성장 루프 실현 가능성, 백테스트 허점, 이식성, 뮤즈·클로드 분업 현실성
- 아래는 Fable 산출물 원문 (편집 없음)

---
### ① 총평

뼈대(재료/요리 분리, 충돌 해소 규칙, 짜깁기 테스트)는 옳다. 그러나 문서는 "책 중심 2-layer"를 선언하고, 실물은 비책 구루 1명(농구천재)만 완성된 3-layer다. 성장 루프는 TODO가 서로를 기다려 v0.1을 만들 수 없는 교착 상태다. 백테스트는 LLM 자체가 결과를 아는 문제를 다루지 않아 현 설계로는 검증이 성립하지 않는다. 공개 깃헙 레포에 `source/`(EPUB/PDF)를 넣는 구조는 저작권 사고 직전이다. 뮤즈·클로드 분업은 리뷰 관점에 있지만 문서 어디에도 정의가 없다.

### ② 발견된 문제점

**높음**

1. **`source/` 저작권 + 공개 레포 조합 (.gitignore 부재)**
   ARCHITECTURE는 원문을 `books/<저자>/<책>/source/`에 두라 하고, OBSIDIAN-MCP-SETUP은 `github.com/kmskr2000-tech/guru-brain`을 clone하라 한다. `.gitignore` 규칙이 어디에도 없다. `git add .` 한 번이면 책 원문이 공개 저장소에 올라간다. 복구해도 히스토리에 남는다.

2. **백테스트의 사후확증 편향을 "정보 차단"으로 막을 수 없다**
   "판단 시점에 알려진 정보만 복원"은 사람용 블라인드다. 판단을 재현하는 LLM은 2020.3 코로나, 2021 BBIG, 2022 베어의 결말을 학습 데이터로 이미 안다. 날짜·국면을 보는 순간 결과를 안다. 게다가 현인의 철학 자체가 결과를 본 뒤 쓰인 글(농구천재 2026년 글이 2018 사이클을 회고)에서 추출됐다. 철학에도 룩어헤드가 들어 있다. 현 설계는 "맞췄다"는 결과만 양산한다.

3. **규칙 개정 루프 = 과적합**
   케이스마다 "어떤 규칙이 오작동했는지 기록 → 규칙 개정"을 같은 10~20개 케이스에서 반복한다. 평가 집합으로 학습하는 것이다. 홀드아웃·사전 등록이 없으니 v5가 v1보다 좋아 보여도 역사 암기일 뿐이다.

4. **성장 루프 부트스트랩 교착 + 버전 재현 불가**
   세계관/말투는 "첫 책 후", 판단 프로세스·conflict-rules는 "캐논 확정 후", 캐논은 "사용자 확정 대기". 책은 0권. 유일한 완성물 농구천재는 책이 아니라 루프에 진입점이 없다(reading-log는 책 전용). 또한 `나성의현인.md` 단일 가변 파일만 있어 백테스트가 요구하는 "철학 v_n으로 재현"이 불가능하다. git tag 규칙도 명시돼 있지 않다.

5. **"책 중심 2-layer" 선언과 실제 구조 불일치**
   캐논 12명 중 한국 블로거·전략가 6명은 저서가 없거나 블로그가 본체다. 실제로는 `gurus/`가 주 레이어가 된다. 그런데 `gurus/`는 "보조", 성장 루프·독서 기록·버전 업 전부 책 전용이다. 또 Layer 1 단위는 책, conflict-rules 단위는 구루(버핏 vs 린치). 같은 저자가 책마다 입장이 바뀌면(버핏 1970s vs 2010s) 어느 단위로 충돌을 적는지 정의가 없다.

6. **뮤즈·클로드 분업 미정의 + 전사 핸드오프 리스크**
   README에 "뮤즈뿐 아니라 클로드"만 있고, 누가 무엇을 쓰고 어떤 파일로 넘기는지 없다. 두 에이전트가 같은 `나성의현인.md`를 편집하면 충돌한다. 핸드오프가 채팅 붙여넣기로 이뤄지면 전사 손상이 생긴다(이 워크스페이스 AGENTS.md에 같은 패턴의 기록이 수십 건). 분업은 파일·깃 단위여야 한다.

**중간**

7. **옵시디언 파일명 충돌**
   모든 책이 `ch01.md`, `index.md`, `principles.md`, `quotes.md`를 가진다. `[[ch01]]`, `[[principles]]`는 두 번째 책부터 모호 링크다. 농구천재 노트도 `관찰 포인트.md`, `하지 않는 것.md`, `서술 구조와 문체.md`처럼 범용 이름이다. 두 번째 구루가 같은 이름을 쓰는 순간 그래프가 섞인다.

8. **허브 문서가 위키링크 대신 백틱 경로를 쓴다**
   README·ARCHITECTURE·USAGE·나성의현인.md(`→ conflict-rules.md`)가 전부 백틱 경로다. 그래프 뷰에서 허브 문서가 고립 노드가 된다. GURU_TEMPLATE의 `[[원칙명]]`은 대응 파일 계층이 없어 전부 끊어진 링크다. GURU_TEMPLATE 저서 경로 `books/{{저자}}/books/{{책제목}}.md`는 ARCHITECTURE의 `books/<저자>/<책제목>/`와 다르다(오타).

9. **"판단 품질" 지표 미정의, 반증 불가 판단**
   스코어카드가 "적중/오판"인데 현인의 기본 어조(농구천재 계승)는 "결론은 모름". 열린 결론은 적중도 오판도 아니다. 평가가 성립하려면 확신도 달린 반증 가능 진술을 강제해야 한다. 베이스라인(개별 구루 렌즈·단순 룰·무지식 모델)과의 비교도 없어 "합성이 뭘 더했는지" 알 수 없다. 케이스는 전부 유명 전환점이라 "아무 일도 없던 시기"의 오경보율을 측정할 수 없다.

10. **이식성: 파생물 외부 반출·용량·링크**
    원문 20~30% 분량의 재구성 노트를 ChatGPT Knowledge·Gemini에 통째 업로드하는 절차다. "외부 업로드 최소화"는 `source/`에만 걸려 있다. Custom GPT는 Knowledge 파일 수 상한이 있어 한 책(ch 10여 개 + 3개)만으로 한도에 걸린다(수치는 공식 문서 확인 필요). `[[링크]]`는 Obsidian 밖에서 의미가 없는데 번들 변환 규칙이 없다. `build_bundle.py` 스펙(포함 순서·제외·크기 상한·버전 헤더)이 문서에 없다. "Cowork은 Google Drive 동기화로 참조 가능"은 근거 없이 단정됐다.

11. **USAGE 읽기 순서가 RAG 도구에서 집행 불가**
    Projects·Custom GPT·Gems는 청크 검색이다. "index.md 먼저, chNN 골라 읽기"는 Claude Code처럼 파일을 직접 여는 환경에서만 성립한다. 도구별 분기가 없다.

12. **정밀 캡처 분량·환각**
    원문 20~30%면 400쪽 책에 80~120쪽 LLM 산출물이다. 책 1권에 며칠, 캐논 12명이면 수개월. 노트에 "LLM 재구성" 신뢰 표식(확인됨/추정/페이지)이 없어, 백테스트와 답변이 환각 위에 설 수 있다.

**낮음**

13. **frontmatter 없음** — `_index.md` 표를 손으로 유지한다. 상태가 두 곳(파일·표)에 있어 어긋난다. Dataview 자동 색인 불가.
14. **상태 범례 불일치** — gurus/_index.md 범례는 `렌즈 보유 → 확정 → 작성 중 → 완료`, 표 값은 `완료/예정/후보`.
15. **reading-log 단일 파일** — 책이 늘면 비대해지고 `[[책]]` 단위 링크가 불가능하다.
16. **농구천재 코퍼스 경로가 vault 밖** — `~/workspace/skills/nonggu-lens/...`는 다른 PC의 Obsidian에서 깨진다. `corpus.db` 비공개인데 경로가 공개 레포에 적혀 있다.
17. **MCP 가이드 미검증 주장** — "Local REST API 플러그인에 MCP 내장"은 플러그인 문서로 확인해야 한다. `https://127.0.0.1:27124`는 자가서명 인증서라 `mcp-remote`가 TLS 검증에서 막힐 가능성이 높다. `claude mcp add`는 API 키를 `~/.claude.json`에 평문 저장한다.
18. **한글 파일명 NFC/NFD** — macOS에서 커밋한 한글 파일명(NFD)과 Windows/Linux(NFC)가 섞이면 `[[링크]]`가 깨진다. `git config core.precomposeunicode true` 안내 없음.
19. **비교 모드 산출물 없음** — "이선엽 vs 윤지호"는 둘 다 파일 없음. 비교 템플릿도 없다.

### ③ 파일별 구체 개선안

**신규 `.gitignore`** (최우선)
```gitignore
**/source/
dist/
.obsidian/workspace.json
.obsidian/workspace-mobile.json
*.db
```
이미 커밋됐다면 `git filter-repo`로 히스토리 제거 후 force push.

**`README.md` — 구조 섹션**
```diff
-## 구조 (책 중심 2-layer)
-- **Layer 1 — 책 코퍼스** (`books/`): ...
-- **Layer 2 — 합성** (`synthesis/`): ...
-- **보조 — 구루 파일** (`gurus/`): 책이 아닌 구루용. 책 중심이 우선.
+## 구조 (소스 2종 + 합성 1층)
+- **소스 A — 책** ([[books/_index|저서 색인]]): 저서가 있는 구루.
+- **소스 B — 구루 렌즈** ([[gurus/_index|구루 캐논]]): 블로거·전략가. 저서 없는 캐논 6명의 본체.
+- **합성** ([[나성의현인]]): 두 소스를 같은 절차(흡수 기록 → 철학 반영 → 버전 업)로 소화한다.
+  버전은 [[synthesis/versions/_index|버전 스냅샷]]에 불변 파일로 보관한다.
```
제약 섹션에 추가:
```markdown
- 외부 AI 도구에 올리는 파일은 `synthesis/*`, 각 책의 `principles.md`·`quotes.md`로 한정. `chNN.md`와 `source/`는 로컬 전용.
```

**`ARCHITECTURE.md`**

(a) 성장 루프를 책·구루 공용으로:
```diff
-## 성장 루프: 독서 → 철학 반영
-1. 정밀 캡처 ... 2. 독서 기록: `synthesis/reading-log.md` ...
+## 성장 루프: 흡수 → 철학 반영 (책·구루 공용)
+1. 소스 완성: `books/<저자>/<책>/` 또는 `gurus/<구루>/`
+2. 흡수 기록: `synthesis/absorb/<YYYYMMDD>-<소스명>.md` (형식은 reading-log 참조)
+3. 철학 반영: `나성의현인.md` 수정. 변경 전 현재 버전을 `synthesis/versions/v0.N.md`로 복사(불변).
+4. 버전 업: 철학 본문·판단 프로세스·conflict-rules 중 하나라도 바뀌면 minor(+0.1). 말투·예시만 바뀌면 patch. git tag `guru-v0.N`.
+5. 검증: 백테스트는 항상 `versions/v0.N.md`를 입력으로 돌린다(가변 파일 금지).
+6. 3권(또는 3구루)마다 **전체 재합성**: 최근 소스 편향을 막기 위해 모든 흡수 기록을 다시 읽고 철학을 처음부터 다시 쓴다.
```
부트스트랩 명시:
```markdown
### v0.0 부트스트랩
첫 책을 기다리지 않는다. 농구천재 렌즈(P1~P6·하지 않는 것)로 v0.0을 작성한다.
세계관/판단 프로세스/conflict-rules의 TODO는 v0.0에서 "단일 구루 상태"로 채우고, 두 번째 소스에서 첫 충돌 규칙이 생긴다.
```

(b) 캡처 분량:
```diff
-분량 목표는 원문의 20~30%
+분량 상한은 원문의 10%. "판단 순간" 단위로 쓰고, 서술·배경은 한 줄로 압축한다.
+각 노트 항목에 신뢰 표식: `[확인 p.NN]` / `[재구성]` / `[추정]`. 백테스트·답변은 `[추정]` 항목을 근거로 쓰지 않는다.
```

(c) 백테스트 섹션 교체:
```markdown
## 검증 루프 (사전 등록 방식)

### 전제: LLM은 결과를 안다
역사 케이스에서 "모른 척"은 불가능하다. 따라서 측정 대상을 바꾼다.
- 측정하지 않는 것: 방향 적중률.
- 측정하는 것: ① 규칙 적용의 일관성(같은 입력에 같은 규칙이 발동하는가) ② 리스크 식별 커버리지(사후 실제 발생한 리스크를 사전 목록에 올렸는가) ③ 금기 준수 ④ 확신도 캘리브레이션(Brier).

### 절차
1. **사전 등록**: 버전 v0.N 확정 → `backtests/v0.N/PREREG.md`에 케이스 목록·채점 기준을 먼저 커밋. 이후 변경 금지.
2. **케이스 집합**: 전환점 10개 + **무사건 기간 10개**(오경보율 측정) + 홀드아웃 5개(규칙 개정에 절대 쓰지 않음).
3. **입력 포장**: 날짜·종목명·지수명을 토큰화(`[T0]`, `[종목A]`)해 재인식을 늦춘다. 완전 차단은 아니므로 결과에 "익명화 수준"을 기록.
4. **반증 가능 출력 강제**: 판단 템플릿에 `확신도 0~100`, `무효화 조건`(이 지표가 X면 내 판단은 틀림) 필수. "결론은 모름"만으로는 미응답 처리.
5. **베이스라인 3종**: 개별 구루 렌즈 답, 철학 없는 동일 모델 답, 직전 버전 v0.N-1 답. 합성이 셋을 이기지 못하면 버전 롤백.
6. **규칙 개정은 홀드아웃 밖에서만**. 개정 후 홀드아웃 재채점으로 과적합 확인.
7. 실행 로그에 모델 ID·온도·프롬프트 해시 기록.

### Track B 주의
브리핑·버틀러 원장·Blue-Red 워치리스트는 vault 밖 사적 기록이다. 사용할 케이스는 `backtests/cases/`에 당시 정보만 발췌해 넣고 출처를 적는다. 본인의 실제 매매 기록은 감정 편향이 있으므로 채점자와 판단자를 분리한다(판단: 현인, 채점: 사람).
```

**`USAGE.md`** — 도구별 분기 추가:
```markdown
## 환경별
- 파일 접근 가능(Claude Code·MCP): 위 순서 그대로.
- RAG 업로드형(Projects·Custom GPT·Gems): 순서 집행 불가. 대신 `나성의현인.md` 상단 frontmatter의 `version`을 답 머리에 표기하고, 근거는 검색된 청크의 `source:` 메타만 인용. 검색되지 않은 책은 "미학습"으로 답한다.

## 거부 템플릿
종목·타이밍·목표주가 질문 → "그 판단은 하지 않는다. 대신 이 상황에서 점검할 질문 3개:" 형식으로 전환.
```

**`PORTABLE.md`**
```diff
-핵심은 두 개만 올리면 된다 ... 책 내용은 쓰는 만큼 `books/`에서 가져간다.
+외부 반출 허용 파일(티어 1): `synthesis/나성의현인.md`, `USAGE.md`, `synthesis/conflict-rules.md`, 각 책 `principles.md`·`quotes.md`.
+로컬 전용(티어 2): `chNN.md`, `index.md`, `source/`. 외부 RAG에 올리지 않는다(저작권·용량).
```
```diff
-## Claude Cowork
-- Google Drive에 guru-brain 폴더를 동기화해 두면 Cowork에서 참조 가능.
+## Claude Cowork
+- (미검증) 로컬 폴더 지정 방식 확인 후 기재. 확인 전까지 Claude Code 경로 사용.
```
```diff
-## ChatGPT — Custom GPT
-2. Knowledge에 책 파일(`books/<저자>/<책>/` 전체) 업로드
+## ChatGPT — Custom GPT
+2. Knowledge에 티어 1 파일만. 파일 수 상한 존재(현재 수치는 OpenAI 문서 확인). 책이 늘면 `build_bundle.py --tier 1`로 1파일 번들.
```
번들 절에 스펙 추가:
```markdown
`build_bundle.py` 규약: 포함 순서 = 나성의현인 → USAGE → conflict-rules → principles/quotes(책 순); `source/`·`chNN.md` 제외; `[[링크]]`를 `## 제목` 앵커로 변환; 헤더에 `version`, 생성일, 포함 파일 해시 기록; 5MB 초과 시 책 단위 분할.
```

**`OBSIDIAN-MCP-SETUP.md`**
```markdown
## 확인 필요
- Local REST API 플러그인의 `/mcp/` 엔드포인트 존재 여부를 플러그인 README에서 확인한 뒤 이 문서를 확정한다.
- 27124는 자가서명 TLS. `mcp-remote` 실패 시 플러그인 설정에서 HTTP(27123) 활성화 후 `http://127.0.0.1:27123/mcp/` 사용(로컬 전용).
- `claude mcp add`는 키를 `~/.claude.json`에 평문 저장. 공유 PC에서는 환경변수 참조로 대체.
```

**`GURU_TEMPLATE.md`**
```diff
+---
+type: guru
+status: 후보 | 예정 | 작성 중 | 완료
+tags: [guru]
+---
 # {{구루명}}
...
-- [[{{책제목}}]] — 한 줄 핵심 (상세: `books/{{저자}}/books/{{책제목}}.md`)
+- [[{{저자}}-{{책약칭}}-index|{{책제목}}]] — 한 줄 핵심
...
-- [[원칙명]] — ...
+- [[충돌 - {{주제}}]] — conflict-rules의 해당 절 (원칙 단위 노트는 두지 않는다)
```
하위 노트 이름 규칙 추가:
```markdown
## 하위 노트 이름
`{{구루명}} - 관찰 포인트.md`, `{{구루명}} - 하지 않는 것.md`, `{{구루명}} - P1 ....md`. 범용 이름 금지(충돌).
```

**`books/_index.md`**
```diff
-장별 `chNN.md` + `index.md` (전체 지도) + `principles.md` + `quotes.md`.
+파일명은 vault 전역 고유: `<저자>-<책약칭>-ch01.md`, `<저자>-<책약칭>-index.md`, `-principles.md`, `-quotes.md`.
+각 파일 frontmatter: `type: book-chapter|book-index|...`, `book:`, `author:`, `status:`, `source_pages:`.
+이 표는 Dataview 쿼리로 대체 가능: `TABLE author, status FROM "books" WHERE type = "book-index"`.
```

**`gurus/_index.md`**
```diff
-상태: `렌즈 보유` → `확정` → 작성 중 → 완료. `후보`는 사용자 승인 후 `예정`으로.
+상태 값은 4개만: 후보 → 예정 → 작성 중 → 완료. (frontmatter `status`와 동일 값)
```

**`gurus/농구천재/*.md`**
- 파일명 변경: `관찰 포인트.md` → `농구천재 - 관찰 포인트.md`, `하지 않는 것.md` → `농구천재 - 하지 않는 것.md`, `서술 구조와 문체.md` → `농구천재 - 문체.md`, `추론 패턴 P1.md` → `농구천재 - P1 첫 등장.md`. 허브의 `[[...]]` 동시 갱신.
- `농구천재.md` 코퍼스 절:
```diff
-- 원본 렌즈: `~/workspace/skills/nonggu-lens/LENS.md`
-- 글 DB: `~/workspace/skills/nonggu-lens/corpus.db`
+- 원본 렌즈·글 DB: 비공개, vault 밖 (nonggu-lens 스킬). 이 vault에는 패턴 요약만 둔다.
```
- 각 P 노트 하단 `## 현인에 반영` 절 추가 → `[[나성의현인]] v0.0 §판단 프로세스 N단계`로 역링크.

**`synthesis/나성의현인.md`**
```diff
+---
+type: persona
+version: 0.0
+sources: [농구천재]
+---
...
-## 충돌 해소 규칙
-→ `conflict-rules.md`
+## 충돌 해소 규칙
+→ [[conflict-rules]]
```
TODO 3곳을 v0.0 단일 구루 내용으로 채운다. 판단 프로세스 초안: `1. 관찰 포인트 중 어느 데이터가 관련인가 → 2. P1~P6 중 발동 패턴 → 3. 수요의 질(P5) 점검 → 4. 밸류·기대치 한 줄 → 5. 무효화 조건 명시`.

**`synthesis/reading-log.md`** → 디렉터리로 전환
```markdown
# 흡수 기록 색인
`synthesis/absorb/<YYYYMMDD>-<소스>.md` 1건 1파일. 책·구루 공용.
추가 필드: `소스 유형: 책 | 렌즈`, `흡수 전 버전`, `흡수 후 버전`, `백테스트 영향: [[backtests/v0.N/...]]`.
```

**`synthesis/conflict-rules.md`**
```diff
 ## 충돌: {{주제}}
+- 규칙 ID: CR-NN (백테스트 로그에서 참조)
+- 도입 버전: v0.N / 개정 이력: v0.N→v0.M (사유, 케이스 ID)
+- 단위: 구루 | 책 | 시기 (예: 버핏-1970s vs 버핏-2010s는 별도 진영)
 - A 진영 ... - B 진영 ... - 해소 규칙 ... - 적용 예 ...
+- 반례: 이 규칙이 틀렸을 케이스 1개 이상
```
파일명도 `충돌 - 집중 vs 분산.md` 개별 노트로 분리하면 `[[충돌 - 집중 vs 분산]]` 링크가 그래프에 잡힌다.

**신규 `WORKFLOW.md`** (뮤즈·클로드 분업)
```markdown
# 분업
| 단계 | 담당 | 산출 파일 | 금지 |
|---|---|---|---|
| 소스 수집·목차·캡처 지시서 | 뮤즈 | `books/<저자>/<책>/BRIEF.md` (목차, 장별 캡처 체크리스트) | 본문 전사 |
| 장별 정밀 캡처 | Claude Code (장문 컨텍스트·파일 도구) | `*-chNN.md` | BRIEF 밖 내용 |
| 누락 검사 | 뮤즈 | `BRIEF.md`의 체크리스트에 ✔ | 노트 직접 수정 |
| 합성·버전 업 | Claude Code 1세션 | `나성의현인.md`, `versions/` | 뮤즈가 동시 편집 |
| opus 리뷰 | `claude -p --model opus` | `absorb/*.md`의 `리뷰:` 절 | — |

## 핸드오프 규칙
- 모든 전달은 파일·깃 커밋. 채팅 붙여넣기로 노트 내용을 옮기지 않는다(전사 손상).
- 쓰기 소유권: 한 파일에 작성자 1명. frontmatter `owner:`로 표기.
- 뮤즈는 BRIEF·색인·검토 메모만 쓴다. Claude Code는 노트·합성만 쓴다.
```

**신규 `synthesis/backtests/_template.md`**
```markdown
---
case_id: KR-YYYY-MM-NN
type: 전환점 | 무사건 | 홀드아웃
version_tested: v0.N
prereg: [[backtests/v0.N/PREREG]]
model: <id> / temp: <n>
---
## 입력 (익명화 수준: 날짜 토큰화 | 종목 토큰화 | 없음)
## 판단 (확신도 0~100, 무효화 조건 필수)
## 발동 규칙 (CR-NN 목록)
## 베이스라인 답 3종
## 채점 (일관성 / 리스크 커버리지 / 금기 / Brier)
## 규칙 개정 제안 (홀드아웃이면 비움)
```

**신규 `synthesis/judgment-rubric.md`** — 위 채점 4축의 0~2점 정의. 백테스트 전에 커밋.

**깃 설정 안내** (README 파일 규칙 절): `git config core.precomposeunicode true`, `.obsidian/`는 `app.json`·`core-plugins.json`만 커밋.
