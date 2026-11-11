# Get started with RoboTest Studio

Use your team's prepared test project with Python 3.12, RoboTest Studio and the
selected browser installed. Your project must provide authentication and the
Appian page fixture used for replay. A recording session's sign-in is not reused.

Activate the project's environment, then start Studio from that project:

```shell
robo-test-studio ui
```

To choose another project, put the project option before the command:

```shell
robo-test-studio --project /path/to/test-project ui
```

Keep Studio on its loopback address. It is a local single-user application.
Ask your project owner to resolve missing dependencies, browsers or application
access before recording. Installation alone does not configure authentication.

## Create and approve a test

1. Create a case with a title and application URL.
2. Choose Record and complete sign-in while capture is paused.
3. Select Start capture in the browser, then perform the scenario.
4. Use Pick visible check or add an expected result in Studio.
5. Stop recording. Review the actions, component names and data bindings.
6. Correct every mapping marked for review. Save the data and replay the draft.
7. Check the business outcome, then choose Approve & Save after a successful replay.
8. Optionally choose Generate Code, or add the approved case to a suite.

Editing a draft requires another successful replay before its next approval.
Existing approved revisions retain the exact reviewed definition and selected data.
Suites and generated tests remain pinned to their approved revisions; save a suite
again to adopt a later approval.

## Data and duplication

Each group uses a shared Excel workbook under `recordings/data/`. Columns identify
fields and each data row has a unique `row_id`. Duplicating a case creates another
draft in the same group with independently assigned rows, not a separate workbook.
Studio edits the selected case's rows while preserving other cases' data.

Use literal values: formula cells are not supported by Studio datasets. Close
Excel before saving from Studio. Keep passwords and authentication tokens out of
recordings and datasets. Existing CORE regression Excel files follow their own
recalculation workflow; they are not Studio datasets.

Continue with [record and review](guide.md), [execution](execution.md), or
[results and evidence](evidence.md).
