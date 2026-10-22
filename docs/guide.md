# Record and review a testcase

## Prepare

Open Studio in your consumer project. Enter the application URL and confirm the
testcase name and Recording ID. Choose the recording timeout and diagnostic
settings. Recording uses a visible browser. Use approved test data.

## Record the workflow

Open the application. If recording starts paused, sign in and select Start
recording on the intended entry page. To include a landing-page warning or
navigation action, enable recording from page load before opening the browser.
Pause for sensitive credential entry, then resume. Record the business actions
in order. Use the panel to pause, resume or save the draft.

## Add a verification

Choose an observable result required by the testcase, such as a visible request
identifier, expected field value or status. Add a verification and review its
expected result. Recording an action does not establish the expected outcome.
At least one explicit approved verification is needed before generation.

## Review the steps

Open the recording in Studio. Review each action, target, input and verification.
Edit incorrect values or mappings, add missing supported steps and remove
unwanted steps. Resolve ambiguity before approval. Approve individual steps or
use Approve all after reviewing every step. Editing step content requires review
and approval again. Save the recording.

## Validate and generate

Validate the recording. Resolve every blocker, including unsupported mappings,
unapproved edits and missing verification. Generate the approved testcase, then
follow [execution](execution.md). Validation confirms supported structure and
approval; it does not prove that the application will satisfy the testcase.

## When a control is unsupported

Keep the draft and provide the relevant step and evidence to your automation
engineer. An approved component mapping may be required. Do not replace a missing
business expectation with a guessed result to pass validation.
