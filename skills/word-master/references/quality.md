# DOCX Quality Gates

Quality review combines semantic package checks with full-page visual review.
Neither substitutes for the other.

## 1. Structural Gate

| Check | Failure condition |
|---|---|
| Package | DOCX is not a valid OPC ZIP or required main parts are missing |
| Spec lock | Approved spec digest does not match the lock |
| Styles | Required semantic roles are direct-formatted or missing |
| Numbering | Lists use typed markers or broken numbering references |
| Tables | Width/grid/cell geometry conflicts or fixed height clips content |
| Media | Relationship is missing, image cannot be opened, or required alt text is absent |
| Navigation | Required bookmark, hyperlink, caption, or field target is unresolved |
| Review markup | Requested comments/tracked changes lack package relationships or anchors |
| Preservation | Native-revision output changes unapproved package features |

## 2. Render Gate

Render every page to PNG and inspect every page at 100% scale.

| Area | Pass condition |
|---|---|
| Text | No clipping, overlap, missing glyphs, orphan headings, or accidental tiny type |
| Pagination | No unintended blank pages, large avoidable gaps, or stranded captions |
| Tables | Readable widths, natural wrapping, repeating headers, adequate padding |
| Figures | Correct crop, resolution, anchoring, caption pairing, and contrast |
| Furniture | Headers, footers, page numbers, rules, and first-page exceptions are consistent |
| Cohesion | Hierarchy, spacing, color, and component treatment match the locked system |

Any layout-sensitive fix invalidates the previous render pass. Rebuild and
inspect the complete page set again.

## 3. Delivery Audits

Run only the audits triggered by the document contract:

| Trigger | Additional audit |
|---|---|
| External distribution | Metadata/privacy and broken-link review |
| Accessibility requirement | Heading order, alt text, table headers, link text, reading order |
| Legal or controlled review | Tracked-change/comment integrity and clean-copy policy |
| Template fill | Required-slot coverage and long-value stress case |
| Native revision | Source/output package preservation diff |

**Hard rule — waiver scope**: only unavailable LibreOffice may waive visual
rendering. Structural validation and triggered delivery audits remain required.
