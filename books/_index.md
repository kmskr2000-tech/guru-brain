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
| 목대균 | 살 것인가, 팔 것인가, 버틸 것인가 | 완료 | `books/목대균/살 것인가, 팔 것인가, 버틸 것인가/` (원문 경로. 웹으로 읽을 때는 한글을 URL 인코딩: `books/%EB%AA%A9%EB%8C%80%EA%B7%A0/%EC%82%B4%20%EA%B2%83%EC%9D%B8%EA%B0%80%2C%20%ED%8C%94%20%EA%B2%83%EC%9D%B8%EA%B0%80%2C%20%EB%B2%84%ED%8B%B8%20%EA%B2%83%EC%9D%B8%EA%B0%80/`) |

완료된 책의 정밀 캡처 파일 (파일명은 vault 전역 고유):
- `<저자>-<책약칭>-principles.md` — 원칙 정리 (대조용 1순위)
- `<저자>-<책약칭>-index.md` — 장별 지도
- `<저자>-<책약칭>-chNN.md` — 장별 정밀 캡처 (ch01~ch25)
- `<저자>-<책약칭>-quotes.md` — 직접 인용 모음

예: 목대균 책의 principles.md =
`books/목대균/살 것인가, 팔 것인가, 버틸 것인가/목대균-바이셀홀드-principles.md`
(웹: `.../books/%EB%AA%A9%EB%8C%80%EA%B7%A0/%EC%82%B4%20%EA%B2%83%EC%9D%B8%EA%B0%80%2C%20%ED%8C%94%20%EA%B2%83%EC%9D%B8%EA%B0%80%2C%20%EB%B2%84%ED%8B%B8%20%EA%B2%83%EC%9D%B8%EA%B0%80/%EB%AA%A9%EB%8C%80%EA%B7%A0-%EB%B0%94%EC%9D%B4%EC%85%80%ED%99%80%EB%93%9C-principles.md`)
