---
description: Deterministic selection among Word Master's four DOCX lifecycles.
---

# Routing Rules

Select one artifact lifecycle from the matrix. Supporting validation and render
stages refine that lifecycle; they are not additional routes.

## 1. Route Matrix

| Route | Request shape | Preconditions | Mutation model | Output contract |
|---|---|---|---|---|
| Generate DOCX | Create a new report, proposal, SOP, manual, form, brief, or other Word document from sources or a topic | Source facts exist or bounded research is permitted | Author a new native DOCX from an approved specification | Project with spec, lock, builder, validation, renders, and final DOCX |
| Create Word Template | Create a reusable Word design/content shell | Reusable-template intent; references are optional | Author a new template workspace without changing references | Template spec plus base DOCX or DOTX and preview renders |
| Fill Native DOCX | Populate a supplied DOCX/DOTX shell, content controls, fields, or explicit placeholders | Source template plus new content | Clone and fill known slots while preserving native structure | New populated DOCX plus fill manifest and validation |
| Revise Native DOCX | Edit, redline, comment on, normalize, or polish an existing document while retaining its identity | Existing DOCX | Apply scoped native edits to a clone | Revised DOCX, change manifest, validation, and renders |

## 2. Discriminators

| Condition | Route |
|---|---|
| Existing DOCX is only source material and may be restructured | Generate DOCX |
| Existing DOCX controls layout and exposes fillable slots | Fill Native DOCX |
| Existing DOCX must keep its structure while wording or formatting changes | Revise Native DOCX |
| Reusable rules or shells are the requested deliverable | Create Word Template |

**Forbidden — fuzzy template treatment**: calling a file a “template” does not
authorize structural inference. Fill only explicit content controls, merge
fields, bookmarks, or documented placeholder tokens. Use Create Word Template
when the request is to extract reusable rules from an ordinary document.

## 3. Ambiguity Boundary

Ask one discriminator question only when the same existing DOCX could
reasonably mean either “replace its slots” or “revise its current content.” Do
not offer a route menu when the request already satisfies one matrix row.
