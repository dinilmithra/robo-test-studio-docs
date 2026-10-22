# Review evidence

Studio can capture page evidence while recording and executing a testcase.
Your consumer project's settings determine which captures are enabled. The
library defaults leave recording, execution and failure snapshots disabled.

## Choose capture settings

Use the recording settings before opening the application and execution settings
before running a testcase. Select the available HTML, image or structured JSON
formats. Before-and-after capture records page state around supported actions;
normal capture records the configured action evidence. Failure capture records
the failed state. Existing execution evidence is reused where possible to avoid
duplicate snapshots for the same failure.

Recording remains visible. Headless and window settings apply to execution.
Changing settings does not retroactively add evidence to earlier actions.

## Inspect a result

Open the run result and its evidence links. Compare the observed page state to
the testcase's approved expected result. An image shows the visible page; HTML
and JSON can help an engineer diagnose a missing or ambiguous component.
A successful capture is evidence of the page state, not a passed business test.

## Handle evidence carefully

Use approved data. Page captures can contain application information even when
credential fields are excluded from recorded input values. Share evidence only
through your project's approved channels. If capture is disabled or fails, the
run may have no snapshot for that step; check the diagnostics.
