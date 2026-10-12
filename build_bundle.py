#!/usr/bin/env python3
"""guru-brain 단일 파일 번들 생성.

    python3 build_bundle.py           # 전체 번들
    python3 build_bundle.py --tier 1  # 티어 1만 (외부 업로드용)

티어 1 (외부 반출 허용): synthesis/나성의현인.md, USAGE.md,
  synthesis/conflict-rules.md, synthesis/judgment-rubric.md,
  synthesis/absorb/, synthesis/versions/,
  books의 *-principles.md / *-quotes.md, gurus/ 렌즈 노트.
티어 2 (로컬 전용): books의 chNN/index, source/, synthesis/backtests/,
  dist/, reviews/.
"""
import argparse
import hashlib
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
DIST.mkdir(exist_ok=True)

TIER2_DIRS = {"source", "dist", "reviews"}
TIER2_SYNTHESIS = {"backtests"}


def is_tier1(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    parts = rel.parts
    if any(d in TIER2_DIRS for d in parts):
        return False
    if parts[0] == "synthesis" and len(parts) > 1 and parts[1] in TIER2_SYNTHESIS:
        return False
    if parts[0] == "books":
        # 책은 principles / quotes만 티어 1
        name = path.name
        return name.endswith("-principles.md") or name.endswith("-quotes.md")
    return True


def slugify(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^0-9a-z가-힣-]", "", s)
    return s


def convert_links(text: str) -> str:
    """[[링크]]를 [표시](#슬러그) 앵커로 변환 (최선 노력)."""

    def repl(m):
        inner = m.group(1)
        if "|" in inner:
            target, label = inner.split("|", 1)
        else:
            target, label = inner, inner
        return f"[{label}](#{slugify(target)})"

    return re.sub(r"\[\[([^\]]+)\]\]", repl, text)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:8]


def read_version() -> str:
    persona = ROOT / "synthesis" / "나성의현인.md"
    m = re.search(r"^version:\s*(\S+)", persona.read_text(encoding="utf-8"), re.M)
    return m.group(1) if m else "unknown"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier", choices=["1", "all"], default="all")
    args = ap.parse_args()
    tier1_only = args.tier == "1"

    collected = []  # (title, rel_path)

    def add(title, rel):
        p = ROOT / rel
        if p.is_file() and (not tier1_only or is_tier1(p)):
            collected.append((title, p.relative_to(ROOT)))

    def add_dir(title, rel, pattern="*.md"):
        d = ROOT / rel
        if not d.is_dir():
            return
        files = sorted(d.rglob(pattern))
        if title and (not tier1_only or any(is_tier1(f) for f in files)):
            collected.append((title, None))
        for p in files:
            if tier1_only and not is_tier1(p):
                continue
            if "source" in p.parts:
                continue
            collected.append((None, p.relative_to(ROOT)))

    add("나성의현인 (페르소나)", "synthesis/나성의현인.md")
    add("사용 프로토콜", "USAGE.md")
    add("충돌 해소 규칙", "synthesis/conflict-rules.md")
    add("판단 채점 루브릭", "synthesis/judgment-rubric.md")
    add("흡수 기록", "synthesis/absorb/_index.md")  # 없으면 무시됨
    add_dir("흡수 기록", "synthesis/absorb")
    add_dir("버전 스냅샷", "synthesis/versions")
    add_dir("책 코퍼스 (principles/quotes)", "books")
    add_dir("구루 렌즈 노트", "gurus")

    parts = []
    hashes = []
    for title, rel in collected:
        if title and rel is None:
            parts.append(f"\n\n# {title}\n")
            continue
        p = ROOT / rel
        body = convert_links(p.read_text(encoding="utf-8"))
        parts.append(f"\n\n## {rel}\n\n<!-- hash: {file_hash(p)} -->\n\n" + body)
        hashes.append(f"{rel}: {file_hash(p)}")

    version = read_version()
    header = (
        "<!-- AI 투자 브레인 단일 번들. 생성: build_bundle.py. 원본은 guru-brain/ -->\n"
        f"<!-- version: {version} | tier: {'1' if tier1_only else 'all'} "
        f"| date: {date.today().isoformat()} -->\n"
        "<!-- 포함 파일 해시:\n" + "\n".join(hashes) + "\n-->\n"
    )
    out = DIST / ("나성의현인-번들-t1.md" if tier1_only else "나성의현인-번들.md")
    out.write_text(header + "\n".join(parts), encoding="utf-8")
    size = out.stat().st_size
    print(f"saved {out} ({size // 1024} KB)")
    if size > 5 * 1024 * 1024:
        print("경고: 5MB 초과. 책 단위 분할을 권장한다.")


if __name__ == "__main__":
    main()
