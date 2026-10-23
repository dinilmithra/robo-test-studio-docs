# Get started with RoboTest Studio

RoboTest Studio provides the visual interface. The `robo-recorder` consumer
project stores your configuration, recordings and generated tests. Studio
currently supports approved Appian component mappings; support for other web
applications requires additional adapters.

## Set up the workspace

An engineer provisions Python 3.12 and the project dependencies once. From the
`robo-recorder` consumer directory:

```powershell
python scripts/setup.py --browser chromium
poetry run appian ui
```

The command opens a local Studio page. This documentation site does not run your
tests or store recordings. The recorder browser is always visible.

## Record

Enter the starting application URL, confirm the generated testcase name and
Recording ID, then open the application. Record supported interactions. Pause
when entering sensitive credentials. Direct navigation does not bypass sign-in.
Recording captures interactions; it does not infer expected business outcomes.

## Review

Open the testcase in Studio. Check the semantic targets and input values. Add
explicit verifications for the results the application must produce. Correct
ambiguous targets and remove unwanted steps. Approve the reviewed step contents.
Approving actions alone does not supply a missing verification. Unsupported
controls need an engineer-maintained mapping.

## Execute

Confirm entry-page readiness and approved test data, then generate and execute
the testcase in Studio. The execution settings apply to the new test run; they
do not change the visible recording browser. Review outcomes and evidence.

Python is an optional export for engineering collaboration; routine review and
execution use the UI. See [execution](execution.md), [evidence](evidence.md), and
the detailed [recording guide](guide.md).
