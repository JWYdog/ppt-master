# Word Master Workflow Design

Word Master applies PPT Master's routed, role-owned, gate-driven design to
native Word documents without copying the SVG slide pipeline.

## 1. Architectural Mapping

| PPT Master idea | Word Master realization |
|---|---|
| Deterministic artifact routing | Generate, Create Template, Fill Native, Revise Native |
| Strategist owns plan and resources | Document Strategist owns facts, outline, representation, style direction, and asset inventory |
| Confirmed spec and lock | `document_spec.md` plus SHA-256-bound `spec_lock.json` |
| Executor realizes approved plan | DOCX Executor builds native Word styles, numbering, tables, sections, fields, and review markup |
| Deterministic checker | Project lock validator plus DOCX package quality checker |
| Visual quality gate | LibreOffice render to PNG and inspection of every page |
| Owning-source recovery | Repair facts/spec, resources, builder, or OOXML patch at its owning phase |

## 2. Why Word Has Its Own Pipeline

Slides are fixed canvases; Word is a flowing document model. Page count is an
output of fonts, styles, section properties, tables, figures, fields, and the
renderer. The Word workflow therefore treats native OOXML semantics and
pagination as first-class constraints instead of authoring page graphics.

## 3. Main Lifecycle

```text
Sources or topic
    -> Document strategy
    -> User confirmation
    -> Immutable spec lock
    -> Resource preparation
    -> Native DOCX builder
    -> Structural validation
    -> Full-page render and inspection
    -> Final DOCX
```

The blocking confirmation occurs before resource acquisition and authoring.
Routine realization choices remain with the DOCX Executor; changing approved
facts, structure, identity, or required native behavior returns upstream.

## 4. Artifact Model

Each generated project retains its source material, approved plan, lock,
prepared assets, reproducible builder, validation reports, rendered QA pages,
and final export. This makes a document repairable and auditable rather than a
one-off binary produced by an opaque prompt.

## 5. Initial Implementation Scope

The first implementation provides route authorities, role contracts, project
initialization and locking, structural DOCX inspection, and LibreOffice/PyMuPDF
rendering. Advanced capabilities such as content-control filling, tracked-change
patching, field materialization, accessibility repair, and visual diffing fit as
route-owned scripts or supporting stages without changing the four top-level
lifecycles.
