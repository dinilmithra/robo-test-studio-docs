# Use the recorder features

Follow these instructions in RoboTest Studio after your workspace is set up.
Use **Record** to capture a workflow, **Testcases** to review it, and **Executions**
to run the approved test. No code editing is required for supported workflows.

## Start a recording

1. Select **Record** and enter the **Application URL** where the workflow begins.
2. Check the **Testcase name** and **Recording ID**. Accept the generated values,
   edit them, or select **Generate new name & ID** for new ones.
3. Choose the **Recording browser** your team uses.
4. Leave **Record from page load** selected to capture landing-page actions.
   Clear it if you want to reach a starting page before recording.
5. Select **Open application & record**. A visible browser opens. Check the
   recorder panel to confirm whether recording is active or paused.

Your existing browser sign-in is not reused. Complete any required sign-in steps
in the new browser. Pause recording before entering sensitive information.

## Pause, resume and save

Use the recording toggle in the browser panel to pause or start recording.
Pause for actions that should not become test steps, then resume before continuing
the workflow. Check **Live capture** in Studio to see saved actions.

Select **Save draft** to save progress while keeping the recording session open.
Select **Save & finish** when you have finished capturing and reviewing the workflow.
If the panel covers an application control, drag its heading to move it.

## Add an expected-result check

1. Perform the action whose result you want to check.
2. Select **Add verification** in the browser panel.
3. Select the item that shows the expected outcome, such as a confirmation
   message, supported field or table cell.
4. Open **Review steps & expected results** and check the captured result.
5. Correct the expected value where available and approve the verification.

Use the expected result from your requirement. For example, check for “Request
submitted” only if that is the confirmation your application is required to show.
A successful click alone does not check the business outcome. At least one
verification must be approved before the testcase can be generated.

## Review and change steps

1. Select **Testcases** and choose your saved recording.
2. Select **Review testcase**, then **Edit step** for the step to change.
3. Check its selected item, entered value and expected result. Correct the
   editable details and select **Save changes**.
4. Select **Approve exact step** after reviewing the updated content.

Saving changed step content clears its approval. Review and approve it again.
Use **Browser review** when you need to add interactions or verifications, remove
steps, or resolve a selection that the editor cannot change.

To remove a step in browser review, expand **Review steps & expected results**,
find the step and select **Remove**. Check that the remaining steps still perform
and verify the intended workflow, then save the recording.

## Approve all reviewed steps

In **Review testcase**, review the complete list and save any edits. Then select
**Approve all reviewed steps**. In the browser panel, the equivalent control is
**Approve all steps**.

Check the result: blocked steps remain pending. Bulk approval does not fix an
unclear selection or create a missing verification. Resolve each remaining issue
before continuing.

## Rename a testcase

Select the testcase, edit **Testcase name**, and select **Save name**. The new name
is saved without changing its Recording ID, test filename or approved steps.

## Compare saved versions

Select **History & compare**, choose a saved version, and select
**Compare with current**. Review the differences before approving updates.
This view compares versions; it does not restore an older version.

## Check readiness and generate the test

Select **Validate** in **Testcases**. Resolve every reported issue, then validate
again. Common messages mean:

| If you see… | Do this |
| --- | --- |
| Add and approve at least one explicit verification | Add an expected-result check and approve it. |
| Review and approve this exact step content | Review and approve the current version of that step. |
| The semantic target is ambiguous | Check which item was captured. Use Browser review or ask your automation support team to make the selection unique. |
| Unsupported component or action | Ask your automation support team for a supported recording approach. |

When ready, select **Generate Python** to prepare the executable test. You do not
need to edit the generated file. **Download Python** is an optional handoff to your
automation team. If replacing a different generated file, review the changes
before selecting **Replace differing Python (keep backup)**.

## Choose recording and execution settings

Action and failure snapshots are off by default. Your consumer application can
enable them in its own project settings; Studio loads those settings when opened
from that project. See [Evidence](evidence.md) for capture setup.

Recording settings apply to the next recording or browser review. Execution
settings apply to a test run. They do not change each other's browser session.

| Setting | How to use it |
| --- | --- |
| Log level | Use INFO for normal work. Choose DEBUG when your support team needs more detail. |
| Timeout (seconds) | Set how long supported operations may wait for the application. |
| Action snapshots | Choose project settings, Off, After each action, or Before and after each action. |
| HTML, PNG and JSON | Select the evidence formats when overriding snapshot settings. PNG provides an image; HTML captures page details; JSON provides structured details. |
| Execution browser mode | Choose Visible browser to watch the run, Headless to run without a visible window, or the project setting. Recording always uses a visible browser. |
| Failure snapshots | Enable or disable failure capture separately and select its formats. |

Use **Reset settings to project defaults** to reload the project's configured
settings into the controls. Session choices do not rewrite your project settings.

## Run the testcase

1. Select **Go to execution** or open **Executions**.
2. Choose the approved testcase and check the execution settings.
3. Review its inputs, available test data and starting-page requirements.
4. Select both confirmation checkboxes when you have completed those reviews.
5. Select **Check readiness**. Resolve any blocking issues.
6. Select **Run testcase** and follow the activity status.

Readiness checks do not prove that your test data is valid or that you are signed
in. Each test run must be able to reach the required starting page.

## Review the result and evidence

Choose a run in **Execution history**. Review its overall result, individual step
results and failure details. Open the available evidence links to inspect the
application state. HTML and JSON evidence download as files. Evidence without a
verified step association appears at run level.

A pass covers the checks you approved. Add another verification if an important
business outcome is still unchecked. Evidence is available only when capture was
enabled for the relevant event.

For more detail, see [Record & Review](guide.md), [Execute](execution.md), and
[Evidence](evidence.md).
