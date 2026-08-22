# Word Master Project Contract

This contract is shared by Generate DOCX and Create Word Template.

## 1. Project Layout

```text
<project>/
|-- project.json
|-- document_spec.md
|-- spec_lock.json
|-- sources/
|-- assets/
|-- build/
|   |-- resource_manifest.json
|   `-- build_docx.py
|-- validation/
|   |-- structure.json
|   `-- render/
`-- exports/
    `-- <deliverable>.docx
```

`document_spec.md` is the human-readable planning authority. `spec_lock.json`
binds its exact SHA-256 digest after user approval. A changed spec invalidates
the lock and blocks authoring until the revised plan is confirmed and relocked.

## 2. Required Specification Sections

| Section | Owns |
|---|---|
| I. Communication Contract | Purpose, audience, document type, language, tone, delivery format |
| II. Sources and Facts | Adopted facts, citations, unresolved items, provenance |
| III. Document Architecture | Front matter, section roster, hierarchy, navigation, appendices |
| IV. Content Plan | Section-level claims, evidence, actions, and approximate length |
| V. Design System | Page size, margins, type scale, colors, spacing, headers/footers |
| VI. Semantic Components | Prose, lists, steps, tables, figures, callouts, forms |
| VII. Native Word Features | Styles, numbering, fields, captions, footnotes, comments, protection |
| VIII. Resources and QA | Local asset inventory and acceptance criteria |

## 3. Lock Contract

`spec_lock.json` contains:

| Field | Meaning |
|---|---|
| `schema_version` | Lock schema version |
| `route` | Selected top-level route |
| `spec_sha256` | Exact digest of `document_spec.md` |
| `locked_at` | UTC timestamp |
| `output_name` | Planned DOCX filename |

**Hard rule**: builders consume only a matching lock. Editing
`document_spec.md` after locking requires another explicit confirmation before
regenerating the lock.

## 4. Ownership

| Artifact | Owner | Consumer |
|---|---|---|
| Sources and user constraints | User / intake | Document Strategist |
| `document_spec.md` | Document Strategist | User gate, resource preparation, DOCX Executor |
| `spec_lock.json` | Confirmation stage | DOCX Executor, validators |
| `resource_manifest.json` | Resource preparation | DOCX Executor |
| Builder and DOCX | DOCX Executor | Quality Reviewer |
| Validation and renders | Quality Reviewer | Delivery gate |
