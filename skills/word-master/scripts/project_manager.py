#!/usr/bin/env python3
"""
Word Master - Project Manager

Initialize, lock, inspect, and validate Word Master project workspaces.

Usage:
    python3 scripts/project_manager.py init <name> [--root projects]
    python3 scripts/project_manager.py lock <project_path> [--output-name file.docx]
    python3 scripts/project_manager.py validate <project_path>

Examples:
    python3 scripts/project_manager.py init annual-report --root projects
    python3 scripts/project_manager.py lock projects/annual-report

Dependencies:
    None (only uses the standard library).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from console_encoding import configure_utf8_stdio  # noqa: E402

SCHEMA_VERSION = "1"
REQUIRED_DIRS = ("sources", "assets", "build", "validation", "exports")
SPEC_SECTIONS = (
    "I. Communication Contract",
    "II. Sources and Facts",
    "III. Document Architecture",
    "IV. Content Plan",
    "V. Design System",
    "VI. Semantic Components",
    "VII. Native Word Features",
    "VIII. Resources and QA",
)


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip()).strip("-").lower()
    if not slug:
        raise ValueError("Project name must contain at least one letter or digit.")
    return slug


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _spec_template(name: str) -> str:
    sections = "\n\n".join(f"## {heading}\n\nTBD" for heading in SPEC_SECTIONS)
    return f"# Document Specification: {name}\n\n{sections}\n"


def init_project(name: str, root: Path, route: str) -> Path:
    """Create a new project workspace and return its absolute path."""
    slug = _slugify(name)
    project = (root / slug).resolve()
    if project.exists():
        raise FileExistsError(f"Project already exists: {project}")
    project.mkdir(parents=True)
    for dirname in REQUIRED_DIRS:
        (project / dirname).mkdir()
    _write_json(
        project / "project.json",
        {
            "schema_version": SCHEMA_VERSION,
            "name": slug,
            "route": route,
            "created_at": datetime.now(timezone.utc).isoformat(),
        },
    )
    (project / "document_spec.md").write_text(_spec_template(slug), encoding="utf-8")
    return project


def lock_project(project: Path, output_name: Optional[str]) -> Path:
    """Hash the approved specification and write the project lock."""
    project = project.resolve()
    spec_path = project / "document_spec.md"
    metadata_path = project / "project.json"
    if not spec_path.is_file() or not metadata_path.is_file():
        raise FileNotFoundError("Project must contain document_spec.md and project.json.")
    spec_text = spec_path.read_text(encoding="utf-8")
    if re.search(r"\bTBD\b", spec_text):
        raise ValueError("document_spec.md still contains TBD placeholders.")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    planned_name = output_name or f"{metadata['name']}.docx"
    if not planned_name.lower().endswith(".docx"):
        raise ValueError("Output name must end with .docx.")
    lock_path = project / "spec_lock.json"
    _write_json(
        lock_path,
        {
            "schema_version": SCHEMA_VERSION,
            "route": metadata.get("route", "generate-docx"),
            "spec_sha256": hashlib.sha256(spec_path.read_bytes()).hexdigest(),
            "locked_at": datetime.now(timezone.utc).isoformat(),
            "output_name": planned_name,
        },
    )
    return lock_path


def validate_project(project: Path) -> dict[str, Any]:
    """Validate project structure and lock integrity."""
    project = project.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    for dirname in REQUIRED_DIRS:
        if not (project / dirname).is_dir():
            errors.append(f"Missing directory: {dirname}/")
    for filename in ("project.json", "document_spec.md"):
        if not (project / filename).is_file():
            errors.append(f"Missing file: {filename}")
    spec_path = project / "document_spec.md"
    if spec_path.is_file():
        spec_text = spec_path.read_text(encoding="utf-8")
        for heading in SPEC_SECTIONS:
            if f"## {heading}" not in spec_text:
                errors.append(f"Missing specification section: {heading}")
        if re.search(r"\bTBD\b", spec_text):
            errors.append("document_spec.md contains TBD placeholders.")
    lock_path = project / "spec_lock.json"
    if not lock_path.is_file():
        errors.append("spec_lock.json is not present; authoring remains blocked.")
    elif spec_path.is_file():
        try:
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
            digest = hashlib.sha256(spec_path.read_bytes()).hexdigest()
            if lock.get("spec_sha256") != digest:
                errors.append("spec_lock.json does not match document_spec.md.")
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"Invalid spec_lock.json: {exc}")
    return {
        "project": str(project),
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage Word Master projects.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize a project.")
    init_parser.add_argument("name", help="Project name.")
    init_parser.add_argument("--root", type=Path, default=Path("projects"), help="Project root.")
    init_parser.add_argument(
        "--route",
        default="generate-docx",
        choices=("generate-docx", "create-template", "fill-native-docx", "revise-native-docx"),
        help="Owning workflow route.",
    )

    lock_parser = subparsers.add_parser("lock", help="Lock an approved specification.")
    lock_parser.add_argument("project_path", type=Path, help="Project workspace path.")
    lock_parser.add_argument("--output-name", help="Planned DOCX filename.")

    validate_parser = subparsers.add_parser("validate", help="Validate a project.")
    validate_parser.add_argument("project_path", type=Path, help="Project workspace path.")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    configure_utf8_stdio()
    args = build_parser().parse_args(argv)
    try:
        if args.command == "init":
            project = init_project(args.name, args.root, args.route)
            print(json.dumps({"project_path": str(project)}, ensure_ascii=False))
            return 0
        if args.command == "lock":
            lock_path = lock_project(args.project_path, args.output_name)
            print(json.dumps({"lock_path": str(lock_path)}, ensure_ascii=False))
            return 0
        report = validate_project(args.project_path)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report["valid"] else 1
    except (FileExistsError, FileNotFoundError, ValueError, OSError, KeyError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
