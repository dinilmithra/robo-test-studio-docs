# Results and evidence

Use Execution history to inspect a run and Recording evidence to inspect a
recording. The evidence table links steps, dataset rows and correlation identifiers.
Use Logs to filter an action's records, or download available before/after HTML.
HTML is downloaded rather than executed inside Studio.

Before action HTML and After action HTML are independent options and default to
off. Diagnostic logs default to INFO. Choose DEBUG for detailed capture and target
resolution records; changing log severity does not enable HTML capture.

```shell
robo-test-studio run --suite regression --html-before --html-after --log-level DEBUG
```

Run definitions, selected data and result metadata are retained beneath
`recordings/runs/`. Execution logs, step records, JUnit reports and diagnostics are
beneath `artifacts/runs/`. Recording diagnostics are beneath `artifacts/<session>/`.
The execution libraries separately control configured screenshots and other evidence.

An event-time snapshot does not prove that Appian finished rendering. Compare it
with the failed step and expected outcome. Evidence may contain business data even
after sanitization; use approved data and sharing channels. Older evidence without
correlation identifiers cannot be reliably linked retroactively. Uncaptured earlier
steps cannot be recovered by enabling diagnostics later.
