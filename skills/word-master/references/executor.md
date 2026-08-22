# DOCX Executor

The DOCX Executor realizes the approved plan as a reproducible native Word
package. It consumes the locked spec and prepared resources without reopening
upstream decisions.

## 1. Authoring Order

1. Verify `spec_lock.json` matches `document_spec.md`.
2. Define sections, page geometry, theme colors, and named styles.
3. Define numbering, table geometry helpers, captions, fields, and reusable
   semantic components.
4. Insert approved content and prepared assets.
5. Save, reopen, and structurally validate the package before render review.

## 2. Native Construction Contract

| Content | Required native representation |
|---|---|
| Headings | Named paragraph styles with a coherent outline level |
| Bullets and steps | Numbering definitions; never typed marker characters |
| Tables | Explicit DXA widths, grid, cell widths, margins, and repeating header when needed |
| Figures | Embedded media with alt text, caption, and stable anchoring |
| Navigation | Real bookmarks, hyperlinks, TOC/REF/PAGEREF fields when required |
| Page structure | Section properties, page breaks, keep rules, headers, and footers |
| Review | Native comments and tracked changes when requested |
| Forms | Content controls or documented fields rather than visual blanks alone |

**Hard rule — no layout by whitespace**: do not use repeated spaces, empty
paragraph stacks, manual bullet characters, or tables whose sole purpose is a
decorative divider when a native property expresses the intent.

**Hard rule — deterministic geometry**: set page size, margins, style spacing,
table widths, image sizes, and header/footer distances explicitly. Do not rely
on application defaults for locked design decisions.

## 3. Recovery

| Failure | Return pointer |
|---|---|
| Wrong fact or missing section | Document Strategist and user confirmation |
| Missing external resource | Resource preparation |
| Wrong native structure or formatting | Builder implementation |
| Render-only defect | Builder implementation, followed by full validation and render |
| Template feature lost during edit | Restore source clone and use targeted OOXML patching |
