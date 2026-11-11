# Execute reviewed tests

Run commands from your prepared test project with its environment activated.

```shell
robo-test-studio run --test example --preview --headed
robo-test-studio run --suite regression --browser chromium --wait-time 90
robo-test-studio generate --test example
```

Replace `example` and `regression` with saved case and suite identifiers. Preview
runs the draft for review; ordinary regression uses approved inputs. The CLI uses
headless execution unless `--headed` is supplied. Recording always uses a visible
browser. The default operation wait is 90 seconds.

Generated pytest adapters are optional and live under
`recordings/tests/generated/`. They pin an approved definition and dataset revision.
Changing a draft does not rewrite the previously approved regression inputs.

The same runner can be used in Jenkins. Agents need the project environment,
browser dependencies, application network access and approved unattended
authentication. Recordings do not bypass MFA or transfer sign-in sessions.
Validate the project on a real agent before relying on scheduled execution.

See [results and evidence](evidence.md) to investigate a failed run.
