# robo-test-studio public documentation

This repository owns the user documentation, existing homepage design, assets,
MkDocs configuration and GitHub Pages workflow for robo-test-studio. It contains no
implementation package or private technical documentation. Public API reference
pages describe how to use published libraries; implementation source is hidden.

## Local setup

Use Python 3.12. Run `python setup.py --help` to see all options.
`python setup.py --build` creates the Poetry environment, installs documentation
dependencies and builds with strict checks. `python setup.py --serve` starts
a local preview; optionally set `--dev-addr 127.0.0.1:8001`.
Poetry installs provider packages from PyPI, without private source checkouts.
Commit the generated `poetry.lock` after the first successful dependency resolution.

## Publish

Create the public `dinilmithra/robo-test-studio-docs` repository and commit only this
folder as its root, using a fresh Git history. In Settings → Pages, select
GitHub Actions. Push to `main` or run Deploy public documentation manually.
The workflow builds this repository and deploys its `site` artifact.
No cross-repository access token is required.

Site: https://dinilmithra.github.io/robo-test-studio-docs/

## Documentation boundary

Keep architecture, internal component matching rules, engineering notes, release
procedures and implementation tests in the private library repository.
Do not copy the private repository or its Git history into this repository.

## Pages workflow

The workflow file is `.github/workflows/deploy-docs.yml`. It installs with
Poetry, checks the lockfile, builds with `mkdocs build --strict`, uploads only
`site/`, and deploys to the `github-pages` environment. It runs on pushes to
`main` or manually from Actions → Deploy public documentation → Run workflow.
Choose `main` for manual publication. The run summary links to the published site.
If a lockfile is committed, CI uses it; otherwise CI resolves one for that run.
Keep `site/` ignored. No personal access token or private repository access is needed.
