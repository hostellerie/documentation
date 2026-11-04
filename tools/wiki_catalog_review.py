#!/usr/bin/env python3
"""Review a local, pre-sanitized Geeklog Wiki 2024 page catalog.

Never opens raw SQL or archives; never uploads, modifies or overwrites input.
Usage: python3 tools/wiki_catalog_review.py wiki-2024-catalogue.csv
"""
import argparse
import csv
from collections import Counter
from pathlib import Path
import sys

REQUIRED = {
    "page_id", "titre_wiki", "namespace", "revision_id",
    "taille_octets", "redirection", "rubrique_proposee",
    "ancien_titre_url", "nouvelle_url", "statut_migration",
}
CANDIDATES = {
    "Plugin_API": "development/plugin-api",
    "Plugin_APIG2": "archive/legacy-api",
    "Plugin_Autoinstall": "development/plugin-installation",
    "Functions.inc_-_Listing_of_the_Plugin_Functions": "development/plugin-api",
    "AddToConfiguration": "development/configuration-api",
    "DatabaseSchema": "development/database",
    "Caching_Template_Library": "development/templates",
    "Webservices_API": "development/webservices",
    "Multi-Site_Setup": "administration/multisite",
    "Integrating_the_Comment_Engine": "development/comments",
    "Static_Pages_Plugin": "plugins/static-pages",
    "Theme_Developers_Guide": "development/themes",
    "Coding_Guidelines": "development/coding-guidelines",
    "Adding_Moderation_Capability": "development/moderation",
}
HISTORICAL = {
    "ConfigFile14", "Coding_StandardsG2", "ThemePort:step_two",
    "Using_Mercurial", "Geeklog_Release_Procedures",
}
FIELDS = [
    "page_id", "titre_wiki", "revision_id", "taille_octets",
    "redirection", "rubrique_initiale", "destination_candidate",
    "priorite_revue", "statut", "ancien_titre_url", "nouvelle_url",
    "decision_editoriale", "notes_revue",
]


def sheet_safe(s):
    # Prevent formula execution when someone opens the generated CSV in Calc/Excel.
    # The source CSV already escapes spreadsheet-dangerous titles with an apostrophe;
    # do not add an additional apostrophe to an already protected value.
    if s.startswith(("=", "+", "-", "@", "\t", "\r")):
        return "'" + s
    return s


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source = args.catalog.resolve()
    output = (args.output or source.with_name("wiki-2024-review.csv")).resolve()
    if source == output:
        parser.error("Output cannot overwrite input")
    if not source.is_file():
        parser.error(f"Catalog not found: {source}")
    with source.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        if not REQUIRED.issubset(reader.fieldnames or []):
            parser.error(f"Missing columns: {sorted(REQUIRED - set(reader.fieldnames or []))}")
        rows = list(reader)
    if len(rows) != 360:
        parser.error(f"Expected 360 public namespace-0 rows, found {len(rows)}; do not continue")
    ids, titles = set(), set()
    out = []
    for n, p in enumerate(rows, 2):
        try:
            page_id = int(p["page_id"])
            namespace = int(p["namespace"])
            revision = int(p["revision_id"])
            size = int(p["taille_octets"])
            redirect = int(p["redirection"])
        except (ValueError, TypeError) as exc:
            parser.error(f"Malformed numeric value at CSV row {n}: {exc}")
        title = p["titre_wiki"]
        if namespace != 0 or redirect not in (0, 1) or size < 0 or page_id < 1 or revision < 0:
            parser.error(f"Invalid page metadata at CSV row {n}")
        if page_id in ids or title in titles:
            parser.error(f"Duplicate id/title at CSV row {n}")
        ids.add(page_id)
        titles.add(title)
        # These are tentative *review suggestions*, never final classifications.
        if redirect:
            dest, priority = "", "redirect-review"
        elif title in HISTORICAL or title.startswith(("SoC_", "Summer_of_Code", "Google_Code-in")):
            dest, priority = "archive/legacy-wiki", "historical"
        elif title in CANDIDATES:
            dest, priority = CANDIDATES[title], "review-first"
        else:
            dest, priority = "", "classify"
        out.append({
            "page_id": str(page_id),
            "titre_wiki": sheet_safe(title),
            "revision_id": str(revision),
            "taille_octets": str(size),
            "redirection": str(redirect),
            "rubrique_initiale": sheet_safe(p["rubrique_proposee"]),
            "destination_candidate": dest,
            "priorite_revue": priority,
            "statut": "a_revoir",
            "ancien_titre_url": sheet_safe(p["ancien_titre_url"]),
            "nouvelle_url": "",
            "decision_editoriale": "",
            "notes_revue": "",
        })
    if sum(int(x["redirection"]) for x in out) != 9:
        parser.error("Expected 9 redirects; review input instead of producing an incomplete report")
    out.sort(key=lambda x: (
        {"review-first": 0, "redirect-review": 1, "historical": 2, "classify": 3}[x["priorite_revue"]],
        -int(x["taille_octets"]),
        x["titre_wiki"].casefold(),
    ))
    with output.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(out)
    print("Geeklog Wiki 2024 review inventory")
    print("Pages:", len(out), "| Redirects:", sum(x["redirection"] == "1" for x in out))
    for key, count in sorted(Counter(x["priorite_revue"] for x in out).items()):
        print(f"  {key}: {count}")
    print("Output:", output)
    print("No SQL/archive opened and no GitHub publication performed.")


if __name__ == "__main__":
    main()
