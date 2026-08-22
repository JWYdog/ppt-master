#!/usr/bin/env python3
"""
Word Master - DOCX Quality Checker

Inspect the structural integrity and common semantic defects of a DOCX package.

Usage:
    python3 scripts/docx_quality_checker.py <file.docx> [--json report.json]

Examples:
    python3 scripts/docx_quality_checker.py exports/report.docx --json validation/structure.json

Dependencies:
    None (only uses the standard library).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any, Optional
from xml.etree import ElementTree as ET

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from console_encoding import configure_utf8_stdio  # noqa: E402

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
WP_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS = {"w": W_NS, "wp": WP_NS, "r": R_NS}
REQUIRED_PARTS = ("[Content_Types].xml", "word/document.xml", "word/styles.xml")
FAKE_LIST_RE = re.compile(r"^\s*(?:[•●▪◦‣⁃]|[-*]\s+|\d+[.)]\s+)")


def _paragraph_text(paragraph: ET.Element) -> str:
    return "".join(node.text or "" for node in paragraph.findall(".//w:t", NS))


def _heading_style_ids(styles_root: ET.Element) -> set[str]:
    """Return paragraph style IDs that represent document headings."""
    heading_ids: set[str] = set()
    based_on: dict[str, str] = {}
    for style in styles_root.findall("w:style", NS):
        if style.get(f"{{{W_NS}}}type") != "paragraph":
            continue
        style_id = style.get(f"{{{W_NS}}}styleId") or ""
        name_node = style.find("w:name", NS)
        style_name = name_node.get(f"{{{W_NS}}}val") if name_node is not None else ""
        outline = style.find("w:pPr/w:outlineLvl", NS)
        parent = style.find("w:basedOn", NS)
        if parent is not None:
            based_on[style_id] = parent.get(f"{{{W_NS}}}val") or ""
        if outline is not None or style_id.lower().startswith("heading") or style_name.lower().startswith("heading"):
            heading_ids.add(style_id)
    changed = True
    while changed:
        changed = False
        for style_id, parent_id in based_on.items():
            if parent_id in heading_ids and style_id not in heading_ids:
                heading_ids.add(style_id)
                changed = True
    return heading_ids


def inspect_docx(path: Path) -> dict[str, Any]:
    """Return a machine-readable DOCX structural quality report."""
    errors: list[str] = []
    warnings: list[str] = []
    metrics = {"paragraphs": 0, "tables": 0, "sections": 0, "drawings": 0}
    if not path.is_file():
        return {
            "file": str(path),
            "valid": False,
            "errors": ["File does not exist."],
            "warnings": [],
            "metrics": metrics,
        }
    if not zipfile.is_zipfile(path):
        return {
            "file": str(path),
            "valid": False,
            "errors": ["File is not a valid OPC ZIP package."],
            "warnings": [],
            "metrics": metrics,
        }
    try:
        with zipfile.ZipFile(path) as package:
            names = set(package.namelist())
            for part in REQUIRED_PARTS:
                if part not in names:
                    errors.append(f"Missing required package part: {part}")
            if "word/document.xml" not in names:
                return {
                    "file": str(path),
                    "valid": False,
                    "errors": errors,
                    "warnings": warnings,
                    "metrics": metrics,
                }
            root = ET.fromstring(package.read("word/document.xml"))
            heading_style_ids: set[str] = set()
            if "word/styles.xml" in names:
                styles_root = ET.fromstring(package.read("word/styles.xml"))
                heading_style_ids = _heading_style_ids(styles_root)
            body = root.find("w:body", NS)
            if body is None:
                errors.append("word/document.xml has no w:body.")
            else:
                paragraphs = body.findall(".//w:p", NS)
                tables = body.findall(".//w:tbl", NS)
                metrics["paragraphs"] = len(paragraphs)
                metrics["tables"] = len(tables)
                metrics["sections"] = len(body.findall(".//w:sectPr", NS))
                metrics["drawings"] = len(body.findall(".//w:drawing", NS))
                for index, paragraph in enumerate(paragraphs, start=1):
                    text = _paragraph_text(paragraph)
                    has_numbering = paragraph.find("w:pPr/w:numPr", NS) is not None
                    style_node = paragraph.find("w:pPr/w:pStyle", NS)
                    style_id = style_node.get(f"{{{W_NS}}}val") if style_node is not None else ""
                    is_heading = style_id in heading_style_ids
                    if text and FAKE_LIST_RE.match(text) and not has_numbering and not is_heading:
                        warnings.append(f"Paragraph {index} appears to use a typed list marker: {text[:60]!r}")
                for index, table in enumerate(tables, start=1):
                    if table.find("w:tblGrid", NS) is None:
                        warnings.append(f"Table {index} has no explicit w:tblGrid.")
                    for row in table.findall("w:tr", NS):
                        height = row.find("w:trPr/w:trHeight", NS)
                        if height is not None and height.get(f"{{{W_NS}}}hRule") == "exact":
                            warnings.append(f"Table {index} contains an exact row height that may clip text.")
                            break
                for index, doc_pr in enumerate(body.findall(".//wp:docPr", NS), start=1):
                    if not (doc_pr.get("descr") or "").strip():
                        warnings.append(f"Drawing {index} has no alternative-text description.")
            if "word/numbering.xml" not in names:
                numbered = root.findall(".//w:numPr", NS)
                if numbered:
                    errors.append("Numbering references exist but word/numbering.xml is missing.")
    except (ET.ParseError, KeyError, OSError, zipfile.BadZipFile) as exc:
        errors.append(f"Package inspection failed: {exc}")
    return {
        "file": str(path.resolve()),
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "metrics": metrics,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect DOCX structure and semantic quality.")
    parser.add_argument("docx", type=Path, help="DOCX file to inspect.")
    parser.add_argument("--json", type=Path, help="Optional JSON report path.")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    configure_utf8_stdio()
    args = build_parser().parse_args(argv)
    report = inspect_docx(args.docx)
    payload = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
