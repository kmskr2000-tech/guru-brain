# AI 투자 브레인 (guru-brain)

좋아하는 투자 구루들의 경험·지식·저서를 종합 학습한 세컨드 브레인.

## 구조 (소스 2종 + 합성 1층)

- **소스 A — 책** ([[books/_index|저서 색인]]): 저서가 있는 구루. 책을 제1소스로 한다.
- **소스 B — 구루 렌즈** ([[gurus/_index|구루 캐논]]): 블로거·전략가. 저서가 없거나 블로그가 본체인 캐논의 제2소스.
- **합성** ([[나성의현인]]): 두 소스를 같은 절차(흡수 기록 → 철학 반영 → 버전 업)로 소화한다.
  버전은 [[synthesis/versions/_index|버전 스냅샷]]에 불변 파일로 보관한다.

## 사용 모드

1. **개별 구루 모드**: "버핏은 이 상황을 뭐라고 했지?"
2. **합성 모드**: "현인, 너는 어떻게 봐?"
3. **비교 모드**: "이선엽 vs 윤지호, 관점이 갈리는데?"

## 이식성

전부 평범한 마크다운이라 뮤즈뿐 아니라 클로드(Projects·Code·Cowork),
ChatGPT(Custom GPT), Gemini(Gems) 등 어떤 AI 도구든 가져갈 수 있다.
자세한 방법은 `PORTABLE.md`, AI가 따라야 할 읽기 순서는 `USAGE.md`,
단일 파일이 필요하면 `build_bundle.py` (`dist/나성의현인-번들.md` 생성).

## 파일 규칙

- 전부 Obsidian 호환 마크다운. 구루·원칙·책 간 연결은 `[[이름]]` 링크와 "관련" 섹션으로.
- 이 폴더를 깃헙 레포로 두면 PC Obsidian에서 vault로 열어 그래프 뷰 탐색 가능.
- 구루 추가: `GURU_TEMPLATE.md` 복사 → 작성 → `gurus/_index.md` 등록 → 필요시 `synthesis/conflict-rules.md` 갱신.
- 책 추가: `books/<저자>/<책제목>/` 아래 장별 정밀 캡처 (요약 아님 — 경험·판단·노하우 전부 구조화). 원문은 각 책 디렉터리의 `source/`에 로컬 보관.
- 깃 설정: `git config core.precomposeunicode true` (macOS 한글 파일명 NFD 문제 방지).
  `.obsidian/`은 `app.json`·`core-plugins.json`만 커밋한다.

## 제약

- 개별 종목 추천·매매 타이밍·목표주가·단기 주가 예측은 하지 않음 (교육·의사결정 위생 중심).
- 인용은 짧게, 출처(책·장) 표기. 저서 원문 대량 복제 금지.
- 외부 AI 도구에 올리는 파일은 티어 1로 한정: `synthesis/나성의현인.md`·`USAGE.md`·`synthesis/conflict-rules.md`·각 책의 `principles.md`·`quotes.md`·`gurus/` 렌즈 노트. `chNN.md`·`index.md`·`source/`는 로컬 전용 (PORTABLE.md 참조).
