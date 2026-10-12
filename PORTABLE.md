# 이식 가이드

브레인은 전부 평범한 마크다운이라 어떤 AI 도구든 가져갈 수 있다.
핵심은 두 개만 올리면 된다: `synthesis/나성의현인.md` + `USAGE.md`.
책 내용은 쓰는 만큼 `books/`에서 가져간다.

## Claude (claude.ai) — Projects

1. 새 Project 생성 (이름: 나성의현인)
2. Project Knowledge에 업로드: `synthesis/나성의현인.md`, `USAGE.md`,
   `synthesis/conflict-rules.md`, 쓰는 책의 `books/<저자>/<책>/` 파일들
3. Custom instructions에 `USAGE.md` 내용을 그대로 붙여넣기

## Claude Code

- 레포를 클론(또는 경로 지정)한 뒤 "USAGE.md를 읽고 따라라"고 지시.
- Skill로 등록도 가능: `~/.claude/skills/나성의현인/SKILL.md`에
  USAGE.md 내용 + guru-brain 경로를 기재.

## Claude Cowork

- Google Drive에 guru-brain 폴더를 동기화해 두면 Cowork에서 참조 가능.

## ChatGPT — Custom GPT

1. GPT 만들기 → Instructions에 `나성의현인.md` + `USAGE.md` 붙여넣기
2. Knowledge에 책 파일(`books/<저자>/<책>/` 전체) 업로드

## Gemini — Gems

- Gem instructions에 위와 동일하게 붙여넣기 + 파일 첨부.

## 단일 파일 번들 (업로드가 번거로운 도구용)

```bash
python3 build_bundle.py
```

`dist/나성의현인-번들.md` 하나가 생성된다. 이 파일 하나만 올리면
페르소나 + 사용법 + 전체 코퍼스가 들어간다. (단, 책이 늘면 용량이 커지므로
많아지면 책 단위로 나눠 올리는 것을 권장)

## 주의사항

- 모델이 약하면 합성 품질이 떨어진다 (원칙 나열에 그치고 충돌 해소가 밋밋해짐).
- 책을 추가하면 각 도구에 다시 반영해야 한다. 자동 동기화는 안 된다.
- 원문(`source/`)은 번들에 포함하지 않는다. 정밀 노트만으로 충분하고,
  저작권상 외부 업로드를 최소화하기 위함이다.
