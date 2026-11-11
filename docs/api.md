# Recorder features and limits

Recorder coverage is narrower than the full RoboAppian component library.
Review the mapping and replay each scenario against your application.

| Component or behavior | Recording support |
| --- | --- |
| Text and date fields | Labeled fields; text/date placeholders and table column context where supported. Date replay fills and immediately blurs. |
| Dropdowns | Semantic option selection, including a rerendered trigger when its option list identifies the owner. |
| Radio buttons and checkboxes | Supported selections and explicit checks. |
| Buttons, links and tabs | Named actions; repeated names require context. |
| Tables | Named native tables with unique read-only row keys and unambiguous columns; unsupported layouts require review. |
| Expected results | Visible checks and supported value, selected and checked-state assertions. |
| Reload and navigation | Capture is reinstalled in the new document and stale transient references are cleared. |
| New browser tabs | Actions retain their tab identity; replay follows tabs opened by the workflow. |
| Dialogs and menus | Supported scoped mappings; nested menu capture can require manual review. |

Complex picker search/result sequences, uploads, calendar navigation, arbitrary
keyboard submissions and embedded frames are not automatically reconstructed.
Do not infer support merely because a visually similar control works. There is no
raw-selector or positional fallback for an ambiguous recorded table target.

Recording remains visible regardless of the execution headless option. Recording
and replay have separate browser sessions, so replay needs its own authentication.
No AI service or MCP server is required to run reviewed tests.
