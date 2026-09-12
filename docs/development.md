# How to develop Klink

Use Python 3.11 for development tools. Klink's runtime supports Python 3.9 and later. Install uv, then create an environment:

```bash
uv venv --python 3.11
source .venv/bin/activate
make develop
make lint
make checks
make coverage
make build
make test-dist
```

On Windows, activate with `.venv\Scripts\activate`. Run `make help` for available targets. Type checking (`make check-types`) is advisory. The `dev` extra remains an alias for `develop`.

## Build the theme demo

```bash
make docs
make serve
```

Open <http://localhost:9090>. The existing Sphinx demo uses Klink's local theme and builds into `docs/build/html`. Warnings fail the build. Check navigation, notebook images, code highlighting, and API links after theme changes.

Regular builds use checked-in notebook exports without rerunning notebooks. After editing a notebook, install Pandoc and run `make notebooks` to regenerate its RST and images from saved outputs. Review the changed notebooks, exports, and images together.

To edit styles, install `lessc`, change `klink/less/klink.less`, run `make css`, then rebuild the demo with `make docs`. Commit the compiled CSS with the LESS changes.

Pull requests build downloadable docs artifacts. Builds on `master` publish to the existing `gh-pages` branch. Download distributions from the Build Status workflow for manual publishing; CI does not upload packages to PyPI.

## Update the template

From a clean branch with development dependencies installed, run:

```bash
copier update --answers-file .copier-answers.yaml --trust
```

Resolve conflicts and review the diff before running the checks above. Preserve Klink's MIT license, version, Python runtime floor, Sphinx theme entry point and assets, top-level tests, and Ruff line length. Keep the existing Sphinx demo build as a project-specific customization instead of replacing it with the template's Yardang build.

`.copier-answers.yaml` records the pure-Python template and pinned revision. The Python Templates Copier Update GitHub App can propose updates once installed for this repository; the command above also supports manual updates.
