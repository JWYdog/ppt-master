---
description: Fill explicit slots in a native DOCX or Word template workspace.
---

# Fill Native DOCX

This route preserves the supplied template's package identity and fills only
known slots.

## Step 1 — Intake and Inventory

Clone the source into a project workspace. Inventory content controls by tag or
alias, merge fields, bookmarks, and documented placeholder tokens. When a Word
Master template workspace is supplied, read its `template_spec.md` and
`slot_manifest.json` together with `base.docx`.

**Forbidden — visual guessing**: blank lines, empty cells, and styled empty
paragraphs are not fillable slots unless the supplied contract declares them.

## Step 2 — Map Content

Write `build/fill_manifest.json` with one row per slot: stable ID, source value,
content type, required status, repetition behavior, and transformation notes.
Stop and ask only when a required slot is unresolved or incompatible with the
supplied content.

## Step 3 — Clone and Fill

Fill a clone through `python-docx` or targeted OOXML patching. Preserve style
IDs, numbering definitions, section properties, headers/footers, relationships,
protection settings, and unrelated custom XML. Do not rebuild the document from
extracted text.

## Step 4 — Validate and Render

Run [`quality.md`](../references/quality.md). Verify that every required slot is
resolved exactly once or according to its repetition rule, compare source and
output package invariants, render all pages, and inspect them. Long-value tests
must not clip, overlap, or create unreadable tables.

## Step 5 — Delivery

Deliver the populated DOCX and retain the original source unchanged. Report any
intentionally changed package feature or unresolved optional slot.
