# Robo Test Studio — clean rewrite

This replaces the previous Studio implementation. It uses `robo-appian-recorder`
for capture, semantic translation, validation and replay. Studio owns suite
operations, approval workflow, Excel data editing and execution orchestration.
All files are stored under the explicit consumer project, never in installed packages.

## Set up the supplied workspace

From `core-recorder`, with Python 3.12:

```powershell
python tools/setup.py --browser chromium
poetry run appian ui
```

The affected Poetry lockfiles were removed because their old resolutions describe
the deleted implementation. Setup regenerates them through Poetry. Dependency
resolution and actual FDA/Appian connectivity were not available in the build
session; setup must succeed in the target environment before use.

The `appian` console command and `python -m robo_test_studio` are equivalent.
Use `appian --project C:\FDA\core-recorder ui` to choose another consumer root.

## Record, review and approve

1. Create a test ID, title and application URL.
2. Click Record. In the visible browser, complete login while capture is paused.
3. Click Start capture in the browser toolbar and perform the Appian scenario.
4. Pick visible checks in the browser or add explicit text checks in Studio.
5. Stop recording from Studio. Review actions, targets and data bindings.
6. Correct any blocked mappings. Use advanced JSON for supported dialog/grid scopes.
7. Save data, then Replay draft. Approval requires a successful replay of the exact
   current definition and data. Do not approve a test solely because clicks succeeded.
8. Approve & Save. Optionally Generate pytest for a consumer-owned adapter.

Every edit removes approval. Approved definition revisions remain under
`testcases/<id>/approved/`. Re-recording preserves the old draft and workbook under
its recording session before replacing them. Old Studio schema recordings are not
silently migrated; retain them as source material and re-record or map explicitly.
The rewrite does not import the removed Studio implementation.

## Data, duplication and regression

Excel files live at `data/<test-id>.xlsx`. Each workbook has unique column names,
a unique `row_id` per row and literal values. A step's `data` key refers to a column.
Edit rows in Studio or edit the consumer workbook directly and reload. Close Excel
before Studio saves. Formula cells and calculated data are not supported. Passwords
and authentication state do not belong in the workbook.

Duplicate creates a new draft and independent workbook. Select tests and save a
suite to include them in regression. Browser, operation timeout and headless mode
are selectable. WAIT_TIME defaults to 90 seconds. A fresh fixture context is used
for each dataset row; separate worker credentials remain possible. Parallel suite
configuration is not exposed by this initial UI.

```powershell
poetry run appian run --suite regression --browser chromium --wait-time 90
poetry run appian run --test conference --preview --headed
poetry run appian generate --test conference
poetry run pytest tests/generated/test_conference.py
```

Each run saves its definition/data snapshots, generated pytest adapter, settings,
exit status, execution log, step status stream and JUnit report under `runs/<id>`.
Framework screenshots/HTML evidence remain governed by existing consumer `.env`
settings and `robo-appian` / `robo-automation` behavior. Studio shows execution logs;
an evidence gallery and automatic AI failure repair are not implemented.

## Jenkins

The consumer Jenkinsfile runs the same command-line runner. Configure the agent
label, checkout layout, project `.venv`, installed browsers, network access and
approved unattended authentication. Interactive MFA cannot be automated by recording
it. The example schedule is commented out; enable it only when you choose to schedule
runs. No Jenkins instance was changed or job created by this rewrite.

## Validation and limits

Run the standalone contract tests from a workspace environment:

```powershell
python -m unittest discover -s ../robo-test-studio/tests -v
```

The tests exercise file ownership, approval invalidation, snapshots, Excel roundtrips,
duplication, semantic validation and mocked public Appian replay. They do not establish
compatibility with a live Appian instance. See the recorder README for capture limits.

Keep the server on its loopback address; it is a local single-user application.
A deployed multi-user service requires separate authentication and job isolation.
