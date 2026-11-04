#!/usr/bin/env python3
"""Create a small LOCAL review package from previously extracted Wiki HTML.

The resulting files contain historical Wiki article bodies and MUST be manually
screened for secrets, personal data, and licensing before sharing or committing.
No content is published by this script.
"""
import argparse
import csv
import html
import re
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote

PRIORITY = (
    "Plugin_API", "Plugin_APIG2", "Plugin_Autoinstall",
    "Functions.inc_-_Listing_of_the_Plugin_Functions",
    "AddToConfiguration", "DatabaseSchema", "Caching_Template_Library",
    "Webservices_API", "Multi-Site_Setup", "Integrating_the_Comment_Engine",
    "Static_Pages_Plugin", "Theme_Developers_Guide",
    "Coding_Guidelines", "Adding_Moderation_Capability",
)


class PreviewParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.level = 0
        self.body = []
        self.found = False

    def handle_starttag(self, tag, attrs):
        if tag == "pre":
            self.level += 1
            self.found = True
        elif self.level:
            self.level += 1

    def handle_endtag(self, tag):
        if self.level:
            self.level -= 1

    def handle_data(self, data):
        if self.level:
            self.body.append(data)

    def handle_entityref(self, name):
        if self.level:
            self.body.append(html.unescape("&" + name + ";"))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--catalog", default="wiki-2024-review.csv", type=Path)
    p.add_argument("--preview", default="wiki-preview-local", type=Path)
    p.add_argument("--out", default="wiki-review-pilot-14.zip", type=Path)
    a = p.parse_args()
    with a.catalog.open(encoding="utf-8-sig", newline="") as file:
        catalog = {row["titre_wiki"]: row for row in csv.DictReader(file)}
    missing = sorted(set(PRIORITY) - catalog.keys())
    if missing:
        p.error(f"Missing catalog entries: {missing}")
    entries = []
    contents = []
    for title in PRIORITY:
        item = catalog[title]
        if item["redirection"] != "0":
            p.error(f"Unexpected redirect: {title}")
        file = a.preview / (quote(title, safe="") + ".html")
        if not file.is_file():
            p.error(f"Missing preview file: {file}. Run wiki_preview.py --all first.")
        parser = PreviewParser()
        parser.feed(file.read_text(encoding="utf-8"))
        if not parser.found:
            p.error(f"Historical wikitext <pre> not found in {file}")
        body = "".join(parser.body)
        if not body.strip():
            p.error(f"Empty wikitext in {file}")
        if len(body) > 500_000:
            p.error(f"Unexpectedly long article: {title}")
        # The bundled text remains WIKITEXT, not modernized Markdown.
        # It uses a .wiki extension so nobody mistakes it for final documentation.
        filename = f"source/{quote(title, safe='')}.wiki"
        contents.append((filename, body))
        entries.append({
            "page_id": item["page_id"],
            "title": title,
            "revision_id": item["revision_id"],
            "source_file": filename,
            "review": "NOT REVIEWED",
        })
    lines = [
        "page_id,title,revision_id,source_file,review"
    ]
    import io
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=list(entries[0]))
    writer.writeheader()
    writer.writerows(entries)
    with zipfile.ZipFile(a.out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("REVIEW-ME-FIRST.txt",
                   "Geeklog historical Wiki — 14 original articles.\n"
                   "NOT modernized documentation. Review for passwords, private data,\n"
                   "copyright and technical obsolescence before uploading or publishing.\n")
        z.writestr("manifest.csv", output.getvalue())
        for filename, body in contents:
            z.writestr(filename, body)
    with zipfile.ZipFile(a.out) as z:
        assert len(z.namelist()) == len(PRIORITY) + 2
    print(f"Prepared {len(PRIORITY)} source articles: {a.out.resolve()}")
    print("Review the package LOCALLY before attaching it to a conversation.")
    print("No repository modification, conversion claim, or public deployment.")


if __name__ == "__main__":
    main()
