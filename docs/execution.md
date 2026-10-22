# Execute and inspect tests

Use Studio's Testcases view to select a recording, review readiness checks and
execute its approved testcase. Existing execution uses pytest and the public
RoboAppian page fixture. Browser resources are isolated per testcase according
to the consumer fixture policy; authentication is not saved or reused.

## Before a run

Resolve blocked mappings, approve explicit verifications, confirm test data and
confirm the entry page. Studio checks browser availability and generated source
before launching. The UI regenerates the approved source so an outdated export
is not silently executed. Applications requiring authentication need an
engineer-configured consumer policy or an approved recorded entry flow.

## Execution settings

`HEAD_LESS` controls test execution; recording and browser review remain visible.
`WAIT_TIME` is in seconds. Browser maximization, viewport dimensions, log level
and evidence capture can be configured through supported Studio controls and
project defaults. Project environment values remain consumer-owned.

Studio shows run status and step events and links available evidence. A completed
click is an action, not a business verification. Review the asserted expected
results when interpreting a pass. Failure evidence has independent settings.

## Engineering handoff

Generated Python uses `robo-appian` public components and pytest. Studio is not
required to execute an exported testcase. `robo_appian.execution` provides
optional step telemetry when Studio launches the run. The component library owns
browser synchronization and execution evidence; Studio owns run orchestration
and the results UI. See [evidence](evidence.md) and the
[RoboAppian API documentation](https://dinilmithra.github.io/robo-appian-docs/).
