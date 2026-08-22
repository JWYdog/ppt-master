#!/usr/bin/env python3
"""
Word Master - DOCX Renderer

Render a DOCX through LibreOffice and rasterize every PDF page to PNG for QA.

Usage:
    python3 scripts/render_docx.py <file.docx> --output-dir <directory> [--emit-pdf]

Examples:
    python3 scripts/render_docx.py exports/report.docx --output-dir validation/render

Dependencies:
    LibreOffice and PyMuPDF.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from console_encoding import configure_utf8_stdio  # noqa: E402


def _find_soffice() -> str | None:
    for command in ("soffice", "libreoffice"):
        resolved = shutil.which(command)
        if resolved:
            return resolved
    if os.name == "nt":
        candidates = (
            Path(os.environ.get("ProgramFiles", "")) / "LibreOffice/program/soffice.exe",
            Path(os.environ.get("ProgramFiles(x86)", "")) / "LibreOffice/program/soffice.exe",
        )
        for candidate in candidates:
            if candidate.is_file():
                return str(candidate)
    return None


def render_docx(docx: Path, output_dir: Path, dpi: int, emit_pdf: bool) -> int:
    """Render a DOCX and return the number of PNG pages written."""
    soffice = _find_soffice()
    if not soffice:
        raise FileNotFoundError("LibreOffice/soffice is unavailable. Install LibreOffice and retry.")
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("PyMuPDF is required. Install it with: pip install PyMuPDF") from exc
    docx = docx.resolve()
    if not docx.is_file():
        raise FileNotFoundError(f"DOCX does not exist: {docx}")
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="word-master-render-") as temp_name:
        temp_dir = Path(temp_name)
        profile_dir = temp_dir / "lo-profile"
        convert_dir = temp_dir / "pdf"
        raster_dir = temp_dir / "raster"
        profile_dir.mkdir()
        convert_dir.mkdir()
        raster_dir.mkdir()
        profile_uri = profile_dir.resolve().as_uri()
        command = [
            soffice,
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(convert_dir),
            f"-env:UserInstallation={profile_uri}",
            str(docx),
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        pdf_path = convert_dir / f"{docx.stem}.pdf"
        if result.returncode != 0 or not pdf_path.is_file():
            detail = (result.stderr or result.stdout or "unknown LibreOffice failure").strip()
            raise RuntimeError(f"LibreOffice conversion failed: {detail}")
        scale = dpi / 72.0
        pdf = fitz.open(pdf_path)
        try:
            for index, page in enumerate(pdf, start=1):
                pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
                pixmap.save(raster_dir / f"page-{index:03d}.png")
            page_count = len(pdf)
        finally:
            pdf.close()
        for previous_page in output_dir.glob("page-*.png"):
            previous_page.unlink()
        for rendered_page in sorted(raster_dir.glob("page-*.png")):
            shutil.copy2(rendered_page, output_dir / rendered_page.name)
        if emit_pdf:
            shutil.copy2(pdf_path, output_dir / pdf_path.name)
    return page_count


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render every DOCX page to PNG.")
    parser.add_argument("docx", type=Path, help="DOCX file to render.")
    parser.add_argument("--output-dir", type=Path, required=True, help="PNG output directory.")
    parser.add_argument("--dpi", type=int, default=144, help="Raster DPI (default: 144).")
    parser.add_argument("--emit-pdf", action="store_true", help="Keep the intermediate PDF.")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    configure_utf8_stdio()
    args = build_parser().parse_args(argv)
    if args.dpi < 72 or args.dpi > 300:
        print("Error: --dpi must be between 72 and 300.", file=sys.stderr)
        return 1
    try:
        page_count = render_docx(args.docx, args.output_dir, args.dpi, args.emit_pdf)
        print(f"Rendered {page_count} page(s) to {args.output_dir.resolve()}")
        return 0
    except (FileNotFoundError, RuntimeError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
