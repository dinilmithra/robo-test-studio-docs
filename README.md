# robo-test-studio public documentation

This repository owns the user documentation, existing homepage design, assets,
MkDocs configuration and GitHub Pages workflow for robo-test-studio. It contains no
implementation package or private technical documentation. Public API reference
pages describe how to use published libraries; implementation source is hidden.

## Local setup

Use Python 3.12. Run `python tools/setup.py --help` to see all options.
`python tools/setup.py --build` creates the Poetry environment, installs documentation
dependencies and builds with strict checks. `python tools/setup.py --serve` starts
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

## Pages configuration error: Not Found

If `actions/configure-pages` reports "Get Pages site failed" or "Not Found",
check that the run belongs to this public docs repository. In this repository,
open Settings → Pages → Build and deployment and select GitHub Actions. Then
run Deploy public documentation on `main`.

A private implementation repository must not run the old `publish-*-docs.yml`
workflow. Remove that obsolete file through Git and commit the deletion; extracting
a new ZIP over an existing checkout does not remove old workflow files. Keep the
native-wheel build workflow. Site source and `.github/workflows/deploy-docs.yml`
are owned by this docs repository. Do not rerun a failed historical private docs
workflow; trigger a new run in the public docs repository instead.

## Setup security updates

Run `python tools/setup.py` with Python 3.12 to secure the project environment.
Setup verifies pip is at least 26.2.2, upgrading older pip through the official
SHA256-pinned wheel before downloading Poetry. Newer stable pip is preserved.
Poetry 2.5.1 tooling requires certifi>=2026.10.19. Existing external Poetry tools
with an outdated CA bundle are not used or modified; setup creates a secure
bootstrap environment where allowed. Appian setup needs `--bootstrap-poetry`
when no secure external Poetry installation is available.

Project dependencies and lockfiles stay under Poetry management. If certifi is
already locked below the security minimum, setup updates that lock through Poetry
and stops if the project constraints cannot resolve a safe version. A project
without certifi in its lockfile does not need to add it solely for the Poetry tool.
Downloads or verification failures stop setup before it reports success.

## Content scope

Publish feature usage, user steps and troubleshooting only. Keep source, API inventories, implementation details and engineering requirements in the private library documentation. The site build uses local user guides and does not introspect library source.

## Standalone setup

Environment creation, secure tooling bootstrap and Poetry validation are included in the project setup implementation. Run `python tools/setup.py --help`; a separate environment helper module is not required. Project setup options and existing environment names are preserved.
