---
description: Create a reusable native Word template workspace.
---

# Create Word Template

This route creates a portable template; it never upgrades or overwrites a
reference document in place.

## Step 1 — Define the Reusable Contract

Read [`project-contract.md`](../references/project-contract.md) and
[`strategist.md`](../references/strategist.md). Distinguish reusable rules from
sample content:

| Layer | Reusable content |
|---|---|
| Identity | Fonts, colors, logo rules, metadata, header/footer treatment |
| Structure | Sections, heading hierarchy, page geometry, numbering, table and figure patterns |
| Slots | Content controls, merge fields, bookmarks, or documented tokens |
| Examples | Non-authoritative sample content used only for preview |

Write `templates/template_spec.md` and a slot inventory. Each slot has a stable
ID, semantic purpose, content type, repetition rule, and optionality.

⛔ **BLOCKING**: confirm the reusable contract and fidelity target before
authoring the template.

## Step 2 — Materialize the Template

Read [`executor.md`](../references/executor.md) and author a new
`templates/base.docx`. A DOTX copy is optional when the toolchain can preserve
its content type safely. Use native styles, numbering, sections, fields, and
content controls; do not represent slots only through visual blank space.

## Step 3 — Validate with Representative Content

Create a disposable filled preview using short, long, missing, and repeated
slot values. Validate structure with `docx_quality_checker.py`, render every
page with `render_docx.py`, and inspect overflow, pagination, table expansion,
headers/footers, and field behavior.

The deliverable contains:

```text
<template_workspace>/
|-- templates/
|   |-- template_spec.md
|   |-- slot_manifest.json
|   `-- base.docx
|-- validation/
|   |-- structure.json
|   `-- render/
`-- exports/
    `-- preview.docx
```

## Step 4 — Delivery

Return the template workspace root, not only `templates/base.docx`. Downstream
Fill Native DOCX consumes the workspace contract and the base package together.
