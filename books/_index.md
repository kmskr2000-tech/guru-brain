# 저서 색인

`books/<저자>/<책제목>/` 형태로 정밀 캡처 저장.
파일명은 vault 전역 고유: `<저자>-<책약칭>-chNN.md` + `<저자>-<책약칭>-index.md` (전체 지도) +
`<저자>-<책약칭>-principles.md` + `<저자>-<책약칭>-quotes.md`.
원문 파일은 각 책 디렉터리의 `source/`에 로컬 보관 (개인 학습용, 외부 공유 금지, `.gitignore`).

## 파일 frontmatter

```yaml
---
type: book-chapter | book-index | book-principles | book-quotes
book: {{책제목}}
author: {{저자}}
status: 후보 | 예정 | 작성 중 | 완료
source_pages: p.NN–p.NN   # 해당 시
---
```

이 표는 Dataview 쿼리로 대체 가능:
`TABLE author, status FROM "books" WHERE type = "book-index"`.

| 저자 | 책 | 상태 | 경로 |
|---|---|---|---|
| - | - | - | - |
