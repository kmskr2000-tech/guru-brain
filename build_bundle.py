#!/usr/bin/env python3
"""guru-brain 단일 파일 번들 생성.

페르소나 + 사용법 + 전체 코퍼스를 dist/나성의현인-번들.md 하나로 합친다.
원문(source/)은 제외한다 (PORTABLE.md 주의사항 참조).
"""
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
DIST.mkdir(exist_ok=True)

parts = []

def add(title, path):
    p = ROOT / path
    if p.is_file():
        parts.append(f"\n\n# {title}\n\n<!-- source: {path} -->\n\n" + p.read_text(encoding="utf-8"))

def add_dir(title, rel):
    d = ROOT / rel
    if not d.is_dir():
        return
    parts.append(f"\n\n# {title}\n")
    for p in sorted(d.rglob("*.md")):
        if "source" in p.parts:
            continue
        rel_p = p.relative_to(ROOT)
        parts.append(f"\n\n## {rel_p}\n\n" + p.read_text(encoding="utf-8"))

add("나성의현인 (페르소나)", "synthesis/나성의현인.md")
add("사용 프로토콜", "USAGE.md")
add("충돌 해소 규칙", "synthesis/conflict-rules.md")
add_dir("책 코퍼스", "books")
add_dir("구루 파일 (보조)", "gurus")

out = DIST / "나성의현인-번들.md"
out.write_text(
    "<!-- AI 투자 브레인 단일 번들. 생성: build_bundle.py. 원본은 guru-brain/ -->\n"
    + "\n".join(parts),
    encoding="utf-8",
)
print(f"saved {out} ({out.stat().st_size // 1024} KB)")
