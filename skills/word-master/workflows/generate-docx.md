---
description: Generate a new native DOCX from sources or a topic.
---

# Generate DOCX

This route owns new-document creation. Read
[`project-contract.md`](../references/project-contract.md), then execute the
steps below in order.

## Step 1 — Intake and Project Initialization

1. Resolve the requested document type, audience, purpose, language, factual
   sources, output name, and any explicit visual or compliance constraints.
2. Convert supplied sources into inspectable text without modifying them.
3. Research only planning-critical gaps when the user permits research; retain
   source URLs and adopted facts in `sources/`.
4. Initialize the project:

```bash
python3 "${SKILL_DIR}/scripts/project_manager.py" init <project_name> --root <project_root>
```

## Step 2 — Document Strategy

Read [`strategist.md`](../references/strategist.md) and switch to Document
Strategist. Write `document_spec.md` with the communication contract, factual
outline, section roster, semantic components, style system, assets, native Word
features, and acceptance criteria.

⛔ **BLOCKING**: present a concise summary of the planned document and wait for
explicit approval. Do not author the DOCX, acquire new assets, or write the lock
before approval.

After approval, create the immutable lock:

```bash
python3 "${SKILL_DIR}/scripts/project_manager.py" lock <project_path>
```

## Step 3 — Resource Preparation

Prepare every approved image, chart, logo, citation record, and data file under
`assets/` or `sources/`. Record its local path, role, provenance, and rights
status in `build/resource_manifest.json`. Missing required material returns to
this step; it is not substituted during authoring.

## Step 4 — Native DOCX Authoring

Read [`executor.md`](../references/executor.md) and
[`quality.md`](../references/quality.md), then switch to DOCX Executor.

1. Write the reproducible builder under `build/`.
2. Apply page geometry and styles before content insertion.
3. Build semantic headings, real numbering, explicit table geometry, sections,
   headers/footers, captions, fields, and accessibility metadata as required.
4. Export a draft to `exports/<name>.docx`.

## Step 5 — Structural and Visual Quality Gate

Run project validation and DOCX structure validation:

```bash
python3 "${SKILL_DIR}/scripts/project_manager.py" validate <project_path>
python3 "${SKILL_DIR}/scripts/docx_quality_checker.py" <project_path>/exports/<name>.docx --json <project_path>/validation/structure.json
```

Render the complete document:

```bash
python3 "${SKILL_DIR}/scripts/render_docx.py" <project_path>/exports/<name>.docx --output-dir <project_path>/validation/render
```

Inspect every rendered page at 100% scale. Repair the owning builder or source,
rebuild, rerun structural validation, and re-render until the checks in
[`quality.md`](../references/quality.md) pass.

**Hard rule — renderer fallback**: only a confirmed missing LibreOffice binary
may waive visual rendering. Record that waiver in `validation/render-waiver.md`
and state it at delivery. Any other render failure must be repaired.

## Step 6 — Delivery

Deliver only the final DOCX unless the user requests sources, validation
reports, or preview files. Report the selected document type, template/style
basis, validation result, render page count, and any explicit waiver.
