# 이식 가이드

브레인은 전부 평범한 마크다운이라 어떤 AI 도구든 가져갈 수 있다.

## 반출 티어

- **티어 1 (외부 반출 허용)**: `synthesis/나성의현인.md`, `USAGE.md`,
  `synthesis/conflict-rules.md`, `synthesis/judgment-rubric.md`,
  `synthesis/absorb/`, `synthesis/versions/`,
  각 책의 `<저자>-<책약칭>-principles.md`·`<저자>-<책약칭>-quotes.md`,
  `gurus/` 렌즈 노트 (패턴 요약 — 원문 아님).
- **티어 2 (로컬 전용)**: 각 책의 `chNN.md`·`index.md`, `source/`,
  `synthesis/backtests/`, `dist/`, `reviews/`. 외부 RAG에 올리지 않는다 (저작권·용량).

## Claude (claude.ai) — Projects

1. 새 Project 생성 (이름: 나성의현인)
2. Project Knowledge에 티어 1 파일 업로드
3. Custom instructions에 `USAGE.md` 내용을 그대로 붙여넣기

## Claude Code

- 레포를 클론(또는 경로 지정)한 뒤 "USAGE.md를 읽고 따라라"고 지시.
- Skill로 등록도 가능: `~/.claude/skills/나성의현인/SKILL.md`에
  USAGE.md 내용 + guru-brain 경로를 기재.

## Claude Cowork

- (미검증) 로컬 폴더 지정 방식 확인 후 기재. 확인 전까지 Claude Code 경로 사용.

## ChatGPT — Custom GPT

1. GPT 만들기 → Instructions에 `나성의현인.md` + `USAGE.md` 붙여넣기
2. Knowledge에 티어 1 파일만 업로드. 파일 수 상한 존재 (현재 수치는 OpenAI 문서 확인).
   책이 늘면 `build_bundle.py --tier 1`로 1파일 번들.

## Gemini — Gems

- Gem instructions에 위와 동일하게 붙여넣기 + 티어 1 파일 첨부.

## 단일 파일 번들 (업로드가 번거로운 도구용)

```bash
python3 build_bundle.py           # 전체 번들
python3 build_bundle.py --tier 1  # 티어 1만 (외부 업로드용)
```

### `build_bundle.py` 규약

- 포함 순서: 나성의현인 → USAGE → conflict-rules → judgment-rubric → principles/quotes (책 순) → gurus 렌즈 노트.
- 제외: `source/`, 티어 2 전체 (`--tier 1` 시).
- `[[링크]]`는 `[표시](#슬러그)` 형태의 앵커로 변환 (최선 노력).
- 헤더에 `version` (나성의현인.md frontmatter), 생성일, 포함 파일 해시를 기록.
- 5MB 초과 시 경고 + 책 단위 분할 권장.

`dist/나성의현인-번들.md` 하나가 생성된다. (단, 책이 늘면 용량이 커지므로
많아지면 책 단위로 나눠 올리는 것을 권장)

## 주의사항

- 모델이 약하면 합성 품질이 떨어진다 (원칙 나열에 그치고 충돌 해소가 밋밋해짐).
- 책을 추가하면 각 도구에 다시 반영해야 한다. 자동 동기화는 안 된다.
- 원문(`source/`)은 번들에 포함하지 않는다. 정밀 노트만으로 충분하고,
  저작권상 외부 업로드를 최소화하기 위함이다.
