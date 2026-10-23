# Execute and inspect tests

## Before a run

1. Select the saved testcase in **Testcases**.
2. Review its steps, inputs and expected results.
3. Resolve blocked selections and approve at least one explicit verification.
4. Select **Generate Python** to prepare the executable test; no code editing is required.
5. Open **Executions**, choose the testcase and review the run settings.
6. Confirm the test data and starting-page requirements using both confirmation checkboxes.
7. Select **Check readiness**, resolve the reported issues, then select **Run testcase**.

Readiness checks do not prove your business data is valid or that you are signed in.
Each run must reach its required starting page. A direct URL does not bypass sign-in,
and a recording browser's session is not reused for execution.

## Choose run settings

Choose a visible browser to watch the run or headless mode to run without a visible
window. Choose the permitted wait time, log level and evidence formats before running.
These execution choices do not change the recording browser. Use **Reset settings
to project defaults** when you want to return to your team's configuration.

## Inspect the result

Select a run in **Execution history**. Review the overall result, individual step
results, error details and available evidence links. A pass covers the checks you
approved. Add another verification when an important business outcome is unchecked.

Before rerunning, check whether the previous attempt created or changed business data.
If the starting page or a control cannot be reached, share the failed step and evidence
with your automation support team.

See [record and review](guide.md) and [evidence](evidence.md).
