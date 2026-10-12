#!/usr/bin/env python3
"""새 책 정밀 캡처 스켈레톤 생성기.

books/<저자>/<책제목>/ 아래에 chNN.md, index, principles, quotes, BRIEF.md, source/를 만들고
books/_index.md 표에 행을 추가한다. 덮어쓰기 없음.
임시 디렉터리에 전부 쓴 뒤 한 번에 옮기므로 중간 실패 시 반쯤 만들어진 책이 남지 않는다.

모드:
  신규 생성   --author --title [--short] [--toc | --chapters]
  장 추가     --author --title --add-chapters "장1,장2"  (기존 파일은 건드리지 않음)

실행 주체와 소유권:
  스켈레톤 생성은 뮤즈가 실행하고, 생성 직후 chNN 등 노트 파일의 소유권은 Claude Code로 넘어간다.
  BRIEF.md와 색인(_index.md)은 뮤즈 소유.
"""
import argparse
import json
import os
import re
import shutil
import sys
import tempfile
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BOOKS = ROOT / "books"
INDEX = BOOKS / "_index.md"
PLACEHOLDER = "| - | - | - | - |"
NO_TOC_TITLE = "(목차 미정)"
SECTIONS = ["판단 순간", "사례·일화", "노하우·기법", "저자의 실수·후회"]
HINT = "<!-- 상황-판단-근거-결과-교훈 구조로 작성 -->"
BAD = set('/\\:*?"<>|#^[]') | {"\0"}

q = lambda v: json.dumps(v, ensure_ascii=False)


def nfc(s):
    return unicodedata.normalize("NFC", s).strip()


def die(msg):
    print(f"오류: {msg}", file=sys.stderr)
    sys.exit(1)


class KoHelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        super().add_usage(usage, actions, groups, prefix="사용법: ")


class KoParser(argparse.ArgumentParser):
    def error(self, message):
        message = (message.replace("the following arguments are required", "필수 인자가 없습니다")
                          .replace("unrecognized arguments", "알 수 없는 인자")
                          .replace("expected one argument", "값이 필요합니다")
                          .replace("not allowed with argument", "다음 인자와 함께 쓸 수 없습니다:")
                          .replace("ambiguous option", "모호한 옵션")
                          .replace("argument ", "인자 "))
        self.print_usage(sys.stderr)
        die(message)


def check_name(label, value):
    if not value:
        die(f"{label}이(가) 비어 있습니다.")
    if any(c in BAD for c in value) or value.startswith(".") or value.endswith((".", " ")):
        die(f"{label}에 파일명으로 쓸 수 없는 문자가 있습니다: {value!r}")


def front(type_, book, author, owner, source_pages=False):
    out = (f"---\ntype: {type_}\nbook: {q(book)}\nauthor: {q(author)}\n"
           f"status: 예정\nowner: {owner}\n")
    if source_pages:
        out += 'source_pages: ""\n'
    return out + "---\n\n"


def split_titles(label, raw):
    if not raw.strip():
        die(f"{label} 값이 비어 있습니다.")
    chapters = [nfc(c) for c in raw.split(",") if c.strip()]
    if not chapters:
        die(f"{label}에서 장 제목을 하나도 읽지 못했습니다.")
    return chapters


def read_chapters(args):
    if args.toc is not None:
        if not args.toc.strip():
            die("--toc 값이 비어 있습니다.")
        p = Path(args.toc).expanduser()
        if not p.is_file():
            die(f"목차 파일을 찾을 수 없습니다: {p}")
        try:
            text = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            die(f"목차 파일을 읽을 수 없습니다: {e}")
        chapters = [nfc(l) for l in text.splitlines() if l.strip()]
        if not chapters:
            die("목차에서 장 제목을 하나도 읽지 못했습니다.")
        return chapters, True
    if args.chapters is not None:
        return split_titles("--chapters", args.chapters), True
    return [NO_TOC_TITLE], False


def toc_rows(start, chapters):
    return [f"{n}. {t}" for n, t in enumerate(chapters, start)]


def check_rows(start, chapters):
    rows = []
    for n, t in enumerate(chapters, start):
        rows.append(f"- [ ] ch{n:02d} {t}")
        rows += [f"  - [ ] {s}" for s in SECTIONS]
        rows.append("  - [ ] source_pages 기입")
    return rows


def link_rows(start, chapters):
    return [f"- Ch {n:02d}. {t}:" for n, t in enumerate(chapters, start)]


def chapter_md(book, author, n, title):
    out = front("book-chapter", book, author, "claude-code", source_pages=True) + f"# Ch {n:02d}. {title}\n"
    for s in SECTIONS:
        out += f"\n## {s}\n\n{HINT}\n"
    return out


def index_md(book, author, chapters):
    out = (front("book-index", book, author, "claude-code")
           + f"# {book} — 전체 지도\n\n## 테제 (한 문장)\n\n\n## 장별 연결\n\n")
    return out + "".join(r + "\n" for r in link_rows(1, chapters))


def principles_md(book, author):
    return (front("book-principles", book, author, "claude-code") + f"# {book} — 원칙\n\n## 원칙 N\n\n"
            "- 원칙:\n- 근거:\n- 반례:\n- 충돌:\n")


def quotes_md(book, author):
    return (front("book-quotes", book, author, "claude-code") + f"# {book} — 인용\n\n"
            "| 문장 | 출처(장·페이지) |\n|---|---|\n")


def brief_md(book, author, chapters, has_toc):
    out = (f"---\ntype: book-brief\nbook: {q(book)}\nauthor: {q(author)}\nowner: muse\n---\n\n"
           f"# {book} 캡처 지시서\n\n## 목차\n\n")
    if has_toc:
        out += "".join(r + "\n" for r in toc_rows(1, chapters))
    else:
        out += "목차 미정 — 확정 후 chNN 추가\n"
    out += "\n## 장별 체크리스트\n\n"
    out += "".join(r + "\n" for r in check_rows(1, chapters))
    out += ("\n## 주의\n\n- BRIEF 밖 내용 금지.\n- 원문 대량 전사 금지 (짧은 발췌만 quotes.md에).\n"
            "- `source/`는 `.gitignore`라 커밋 안 됨.\n")
    return out


def insert_in_section(text, heading, rows, drop_prefix=None):
    """heading 섹션의 마지막 내용 줄 뒤에 rows 삽입. 섹션이 없으면 None."""
    lines = text.split("\n")
    try:
        h = lines.index(heading)
    except ValueError:
        return None
    end = next((i for i in range(h + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    if drop_prefix:
        body = [l for l in lines[h + 1:end] if not l.startswith(drop_prefix)]
        lines[h + 1:end] = body
        end = h + 1 + len(body)
    last = h
    for i in range(h + 1, end):
        if lines[i].strip():
            last = i
    lines[last + 1:last + 1] = rows
    return "\n".join(lines)


def atomic_write(path, text):
    """같은 디렉터리의 임시 파일에 쓴 뒤 os.replace로 교체."""
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.tmp-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        if path.exists():
            shutil.copymode(path, tmp)
        else:
            os.chmod(tmp, 0o644)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def update_index(author, book):
    """True: 행 추가됨, False: 건너뜀."""
    if not INDEX.is_file():
        print(f"경고: {INDEX} 가 없어 색인 갱신을 건너뜁니다.", file=sys.stderr)
        return False
    lines = INDEX.read_text(encoding="utf-8").split("\n")
    for l in lines:
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if l.lstrip().startswith("|") and len(cells) >= 2 and cells[0] == author and cells[1] == book:
            print(f"경고: _index.md에 이미 '{author} / {book}' 행이 있어 건드리지 않습니다.", file=sys.stderr)
            return False
    row = f"| {author} | {book} | 예정 | `books/{author}/{book}/` |"
    ph = next((i for i, l in enumerate(lines) if l.strip() == PLACEHOLDER), None)
    if ph is not None:
        lines.insert(ph, row)
    else:
        last = max((i for i, l in enumerate(lines) if l.lstrip().startswith("|")), default=None)
        if last is None:
            print("경고: _index.md에서 표를 찾지 못해 색인 갱신을 건너뜁니다.", file=sys.stderr)
            return False
        lines.insert(last + 1, row)
    try:
        atomic_write(INDEX, "\n".join(lines))
    except OSError as e:
        print(f"경고: _index.md 갱신에 실패했습니다: {e}", file=sys.stderr)
        return False
    return True


def create_book(args, author, title):
    short = nfc(args.short) if args.short else "".join(title.split())[:12]
    check_name("--short", short)
    chapters, has_toc = read_chapters(args)

    book_dir = BOOKS / author / title
    if book_dir.exists():
        die(f"이미 존재합니다: {book_dir} (덮어쓰기 없음)")

    prefix = f"{author}-{short}"
    clash = list(BOOKS.rglob(f"{prefix}-*.md"))
    if clash:
        die(f"파일명 접두사 '{prefix}'가 이미 사용 중입니다: {clash[0]} — --short로 다른 약칭을 지정하세요.")
    if not args.short:
        print(f"약칭: {short} (기본값 — 다르게 쓰려면 --short 지정)")

    files = {}
    for n, t in enumerate(chapters, 1):
        files[f"{prefix}-ch{n:02d}.md"] = chapter_md(title, author, n, t)
    files[f"{prefix}-index.md"] = index_md(title, author, chapters)
    files[f"{prefix}-principles.md"] = principles_md(title, author)
    files[f"{prefix}-quotes.md"] = quotes_md(title, author)
    files["BRIEF.md"] = brief_md(title, author, chapters, has_toc)

    parent = book_dir.parent
    try:
        parent.mkdir(parents=True, exist_ok=True)
        tmp = Path(tempfile.mkdtemp(prefix=f".{title}.tmp-", dir=parent))
    except OSError as e:
        die(f"임시 디렉터리를 만들 수 없습니다: {e}")
    ok = False
    try:
        tmp.chmod(0o755)
        for name, body in files.items():
            (tmp / name).write_text(body, encoding="utf-8")
        (tmp / "source").mkdir()
        os.rename(tmp, book_dir)
        ok = True
    except OSError as e:
        die(f"책 디렉터리 생성에 실패해 정리했습니다: {e}")
    finally:
        if not ok:
            shutil.rmtree(tmp, ignore_errors=True)

    created = [book_dir / n for n in files] + [book_dir / "source"]
    if update_index(author, title):
        created.append(INDEX)

    print("생성/갱신된 파일:")
    for p in created:
        print(f"  {p}")
    print("안내: source/ 는 .gitignore(**/source/)가 적용되어 커밋되지 않습니다.")


def add_chapters(args, author, title):
    new = split_titles("--add-chapters", args.add_chapters)
    if args.short:
        die("--short는 --add-chapters와 함께 쓸 수 없습니다 (기존 파일의 약칭을 따릅니다).")
    book_dir = BOOKS / author / title
    if not book_dir.is_dir():
        die(f"기존 책 디렉터리를 찾을 수 없습니다: {book_dir}")

    idx = sorted(book_dir.glob("*-index.md"))
    if len(idx) != 1:
        die(f"index 파일을 하나로 특정할 수 없습니다 ({len(idx)}개): {book_dir}")
    prefix = idx[0].name[: -len("-index.md")]

    nums = [int(m.group(1)) for p in book_dir.glob(f"{prefix}-ch*.md")
            if (m := re.fullmatch(re.escape(prefix) + r"-ch(\d+)\.md", p.name))]
    start = max(nums, default=0) + 1

    brief_p = book_dir / "BRIEF.md"
    if not brief_p.is_file():
        die(f"BRIEF.md를 찾을 수 없습니다: {brief_p}")
    try:
        brief = brief_p.read_text(encoding="utf-8")
        index = idx[0].read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        die(f"기존 파일을 읽을 수 없습니다: {e}")

    brief = insert_in_section(brief, "## 목차", toc_rows(start, new), drop_prefix="목차 미정")
    if brief is not None:
        brief = insert_in_section(brief, "## 장별 체크리스트", check_rows(start, new))
    index = insert_in_section(index, "## 장별 연결", link_rows(start, new))
    if brief is None or index is None:
        die("BRIEF.md 또는 index의 섹션('## 목차', '## 장별 체크리스트', '## 장별 연결')을 찾지 못했습니다.")

    new_files = {book_dir / f"{prefix}-ch{n:02d}.md": chapter_md(title, author, n, t)
                 for n, t in enumerate(new, start)}
    for p in new_files:
        if p.exists():
            die(f"이미 존재합니다: {p} (덮어쓰기 없음)")

    written = []
    try:
        for p, body in new_files.items():
            with open(p, "x", encoding="utf-8") as f:
                f.write(body)
            written.append(p)
        atomic_write(brief_p, brief)
        atomic_write(idx[0], index)
    except OSError as e:
        for p in written:
            p.unlink(missing_ok=True)
        die(f"장 추가에 실패해 새 장 파일을 정리했습니다: {e}")

    print(f"ch{start:02d}부터 {len(new)}개 장을 추가했습니다.")
    print("생성/갱신된 파일:")
    for p in [*new_files, brief_p, idx[0]]:
        print(f"  {p}")


def main():
    ap = KoParser(description="새 책 정밀 캡처 스켈레톤을 생성한다.", add_help=False,
                  formatter_class=KoHelpFormatter)
    ap._optionals.title = "옵션"
    ap.add_argument("-h", "--help", action="help", help="도움말을 표시하고 종료합니다")
    ap.add_argument("--author", required=True, help='저자명 (예: "하워드 막스")')
    ap.add_argument("--title", required=True, help='책 제목 (예: "투자에 대한 생각")')
    ap.add_argument("--short", help="파일명용 책 약칭 (기본: 제목에서 공백 제거 후 12자)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--toc", help="목차 텍스트 파일 (줄 단위 장 제목)")
    g.add_argument("--chapters", help="쉼표(,) 구분 장 제목")
    g.add_argument("--add-chapters", dest="add_chapters",
                   help="기존 책에 장 추가 (쉼표 구분 장 제목, 마지막 chNN 다음 번호부터)")
    args = ap.parse_args()

    author, title = nfc(args.author), nfc(args.title)
    check_name("--author", author)
    check_name("--title", title)

    if args.add_chapters is not None:
        add_chapters(args, author, title)
    else:
        create_book(args, author, title)


if __name__ == "__main__":
    main()
