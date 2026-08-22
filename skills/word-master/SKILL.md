---
name: word-master
description: >
  Routed workflow for creating, templating, filling, and revising native Word
  DOCX documents with explicit content planning, OOXML-preserving authoring,
  structural validation, and full-page render review. Use for Word reports,
  proposals, manuals, SOPs, forms, and reusable DOCX templates. Do not use for
  slide decks or PDF-only deliverables.
metadata:
  version: "0.1.0"
---

# Word Master Skill

Word Master turns source material or an existing Word package into a native,
editable DOCX. This entry owns route selection and shared execution discipline;
the selected workflow owns the concrete steps and gates.

## Mandatory Load Order

**Hard rule - paths before commands**: retain the absolute directory containing
this file as `SKILL_DIR`. Expand every command through that path; never assume a
repository checkout or a current working directory.

1. Read this file.
2. Read [`workflows/routing.md`](workflows/routing.md).
3. Select exactly one top-level route.
4. Read only the selected route and the references it explicitly activates.

| Route | Runtime authority |
|---|---|
| Generate DOCX | [`workflows/generate-docx.md`](workflows/generate-docx.md) |
| Create Word Template | [`workflows/create-template.md`](workflows/create-template.md) |
| Fill Native DOCX | [`workflows/template-fill-docx.md`](workflows/template-fill-docx.md) |
| Revise Native DOCX | [`workflows/native-revise-docx.md`](workflows/native-revise-docx.md) |

## Global Execution Discipline

1. Follow the selected authority in order and stop at every `BLOCKING` gate.
2. Preserve user-supplied facts, wording constraints, references, template
   identity, and authorization boundaries.
3. Treat research and external assets as upstream preparation. The DOCX
   Executor never invents missing facts or acquires replacement resources while
   authoring.
4. Build native Word semantics: styles, numbering, tables, sections, captions,
   fields, footnotes, comments, and tracked changes remain native when used.
5. Never overwrite a supplied DOCX or template. Write a new deliverable under
   the project `exports/` directory.
6. A DOCX is not ready because its XML parses. Run structural validation, render
   every page to PNG, inspect every page, repair defects, and re-render.

## Shared Artifact Contract

Generate and template routes use the workspace defined in
[`references/project-contract.md`](references/project-contract.md). Fill and
revise routes may use a lighter workspace, but still retain the source package,
an operation manifest, validation reports, render output, and final export.

## Global Communication Rules

- Match the user's chat language and source language unless explicitly
  overridden.
- Ask only about choices that materially change facts, audience, purpose,
  document type, template fidelity, or review mode.
- Before switching roles, read the role reference and report the role switch:

```markdown
## [Role Switch: <Role Name>]
Reading role definition: references/<filename>.md
Current task: <brief description>
```

## Runtime Dependencies

Use the active workspace's supported Python runtime. The baseline package uses
`python-docx`, `lxml`, and PyMuPDF; visual rendering additionally requires
LibreOffice. Run the same command with `python` when `python3` is unavailable.
