---
description: Revise an existing DOCX while preserving its native structure.
---

# Revise Native DOCX

Use this route for scoped wording edits, formatting cleanup, comments, tracked
changes, accessibility fixes, metadata cleanup, or document-wide polish that
must retain the existing document's identity.

## Step 1 — Establish the Change Contract

Clone the source and write `build/change_manifest.json`. Classify each requested
operation as content, style, structure, review markup, accessibility, privacy,
or field/navigation behavior. Record whether delivery is `clean`, `tracked`,
`commented`, or a combination explicitly requested by the user.

## Step 2 — Apply Minimal Native Edits

Read [`executor.md`](../references/executor.md). Prefer the smallest operation
that preserves surrounding runs, styles, bookmarks, fields, numbering,
relationships, section properties, and review markup. Use targeted OOXML when
`python-docx` would flatten a required feature.

**Forbidden — silent regeneration**: do not reconstruct the document from
extracted text or replace all styles unless the user explicitly requests a
major redesign. A redesign request routes to Generate DOCX when structural
identity no longer needs to be preserved.

## Step 3 — Preservation Audit

Compare source and output package facts appropriate to the change contract:
page geometry, sections, headers/footers, styles, numbering, comments, tracked
changes, fields, bookmarks, media, custom XML, and protection. Every difference
must be requested, mechanically necessary, or recorded in the manifest.

## Step 4 — Render and Review

Read [`quality.md`](../references/quality.md), render every output page, and
inspect it. For layout-sensitive edits, compare source and output renders.
Comments also require structural checks because headless rendering may not show
them.

## Step 5 — Delivery

Deliver a new DOCX and a concise change summary. Never overwrite the source.
