# Robo Appian Recorder

A new library for capturing Appian interactions and translating them into reviewed
semantic operations. No implementation from the former Studio recorder is reused.

Dependency direction: `core-recorder -> robo-test-studio -> robo-appian-recorder -> robo-appian`.

Public contract:

- `translate(event, sequence)` returns a semantic step and optional data binding.
- `validate(document, approved=False)` reports unsupported targets and missing checks.
- `fingerprint(document)` identifies a definition independently of its approval stamp.
- `replay(page, document, data, timeout=90, report=None)` executes public `robo-appian`
  component calls. It requires an approved definition and all bound data columns.

Only the recording adapter (`browser.py`, `capture.js`) uses raw browser APIs.
Regression replay uses public `robo-appian` APIs; consumer tests never import Playwright.
Each recording launches a separate, non-persistent context. Regression inherits the
consumer's function-scoped Appian fixture; credentials and sessions are not shared.

## Recording

Studio launches the worker with an explicit consumer output location. In its browser,
complete login while capture is paused, then click **Start capture**. Pause before
logout or other operations outside the scenario. Use **Pick visible check** to record
an explicit expected component. Stop from Studio to flush the active field and save.

The initial adapter supports labeled text/date inputs, checkbox/radio selection,
Appian dropdown option events, named buttons/links/tabs and explicit visible checks.
Date replay immediately blurs after fill. Inputs are parameterized rather than
embedded as Python literals.

## Deliberate limits

This is a new implementation requiring validation on representative Appian screens.
Complex picker search/result flows, calendar navigation, nested menus, keyboard-only
submissions, ARIA-only controls, uploads, cross-frame/popup workflows and ambiguous
labels are not automatically reconstructed. They require a verified mapping or
extension before approval. Grid actions are blocked until explicit semantic grid,
row-key and column mappings are supplied. No nth(), generated ID or raw selector
fallback is used in saved tests.

A recording is not a video or full replay of every browser event. Assertions must
be selected or added by the user. Password/secret values are excluded. Do not record
login credentials or authentication tokens as business data.

MCP and LLM access are not required. An optional future MCP adapter can delegate to
`robo-appian`; it should not own Appian execution logic.
