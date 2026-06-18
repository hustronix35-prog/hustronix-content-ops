#!/usr/bin/env python3
"""Fetch and store a URL or manual content as a raw source."""

from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "marketing.db"
VAULT_RAW = ROOT / "vault" / "raw_sources"


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []
        self._skip = False

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in ("script", "style", "noscript"):
            self._skip = True

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style", "noscript"):
            self._skip = False

    def handle_data(self, data: str) -> None:
        if not self._skip:
            text = data.strip()
            if text:
                self._chunks.append(text)

    def text(self) -> str:
        return "\n".join(self._chunks)


def fetch_url(url: str) -> tuple[str, str]:
    req = Request(url, headers={"User-Agent": "HustronixMarketingOS/1.0"})
    with urlopen(req, timeout=30) as resp:
        html = resp.read().decode("utf-8", errors="replace")

    title_match = re.search(r"<title[^>]*>([^<]+)</title>", html, re.I)
    title = title_match.group(1).strip() if title_match else url

    parser = _TextExtractor()
    parser.feed(html)
    content = parser.text()
    if len(content) < 100:
        content = re.sub(r"<[^>]+>", " ", html)
        content = re.sub(r"\s+", " ", content).strip()

    return title, content[:50000]


def store_source(
    title: str,
    content: str,
    source_type: str,
    source_url: str | None,
    tags: str | None,
) -> int:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    cur = conn.execute(
        """INSERT INTO raw_sources (source_type, source_url, title, content, date, tags)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (source_type, source_url, title, content, date, tags),
    )
    row_id = cur.lastrowid
    conn.commit()
    conn.close()

    VAULT_RAW.mkdir(parents=True, exist_ok=True)
    md_path = VAULT_RAW / f"{row_id}.md"
    md_path.write_text(
        f"# {title}\n\n"
        f"- **Type:** {source_type}\n"
        f"- **URL:** {source_url or 'N/A'}\n"
        f"- **Date:** {date}\n"
        f"- **Tags:** {tags or ''}\n\n"
        f"## Content\n\n{content}\n",
        encoding="utf-8",
    )
    return row_id


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest content into raw_sources")
    parser.add_argument("source", nargs="?", help="URL or omit when using --file")
    parser.add_argument("--type", default="article", dest="source_type")
    parser.add_argument("--title", help="Title for file/manual ingest")
    parser.add_argument("--file", help="Read content from local file")
    parser.add_argument("--tags", help="Comma-separated tags")
    args = parser.parse_args()

    if args.file:
        path = Path(args.file)
        content = path.read_text(encoding="utf-8")
        title = args.title or path.stem
        row_id = store_source(title, content, args.source_type, None, args.tags)
    elif args.source:
        if args.source.startswith("http://") or args.source.startswith("https://"):
            title, content = fetch_url(args.source)
            row_id = store_source(
                title, content, args.source_type, args.source, args.tags
            )
        else:
            print("Provide a valid http(s) URL or use --file", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

    print(f"Ingested raw_source id={row_id}")


if __name__ == "__main__":
    main()
