# Get started with RoboTest Studio

RoboTest Studio lets you record, review and execute supported Appian workflows.
Ask your project owner to prepare the test environment and application access.
Support for other web applications depends on available adapters.

## Open Studio

From your prepared test project, run:

```shell
poetry run appian ui
```

Studio opens locally. This documentation site does not run tests or store recordings.
Recording always opens a visible browser. Use the project settings supplied by your team.

## Record

Enter the starting application URL, confirm the generated testcase name and
Recording ID, then open the application. Record supported interactions. Pause
when entering sensitive credentials. Direct navigation does not bypass sign-in.
Recording captures interactions; it does not infer expected business outcomes.

## Review

Open the testcase in Studio. Check the selected controls and input values. Add
explicit verifications for the results the application must produce. Correct
ambiguous targets and remove unwanted steps. Approve the reviewed step contents.
Approving actions alone does not supply a missing verification. Ask your automation support team about unsupported controls.

## Execute

Confirm entry-page readiness and approved test data, then generate and execute
the testcase in Studio. The execution settings apply to the new test run; they
do not change the visible recording browser. Review outcomes and evidence.

Python is an optional export for engineering collaboration; routine review and
execution use the UI. See [execution](execution.md), [evidence](evidence.md), and
the detailed [recording guide](guide.md).
