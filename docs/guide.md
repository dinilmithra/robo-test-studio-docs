# Record and review a workflow

Start with a short scenario and an explicit expected business result. Complete
login while capture is paused, then select Start capture. Pause again before
performing actions that should not belong to the test.

## Review the captured steps

Check component names, field values, action order and expected results. A captured
click is not proof that the requested transaction succeeded. Review every blocked
mapping before replay and approval; do not remove a check just to make a run pass.

Use labeled controls where possible. Repeated names need a unique dialog or table
context. Table actions need a named table, a unique business row value and a named
column. Ambiguous tables remain blocked for review. See [recorder features](api.md).

## Reloads and navigation

Capture is installed in each new document. After a reload or navigation, interact
with the newly rendered controls. Recording observes interactions; it is not a
complete recording of browser Back, Refresh or arbitrary address-bar actions.
Confirm that replay reaches the same page through the recorded workflow.

When an action opens another tab, recording identifies actions in that tab
separately. Replay waits for the corresponding new tab and can return to the
original tab for later actions. Keep tab-opening actions inside the captured
scenario. Manually opened tabs and tabs opened during paused login need review;
replay must be able to reproduce how the required tab was opened.

## Save and generate

Stop recording to flush the active field, then save and replay the draft. Approval
requires a successful replay of the current definition and selected data.
Generate Code creates a pytest adapter for that approved revision. It does not
produce a second independent implementation of the recorded workflow.

Unsupported controls, embedded frames and complex picker or keyboard workflows
need a verified extension. Representative live Appian validation is still required.
