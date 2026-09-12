.DEFAULT_GOAL := help
.PHONY: develop requirements build install lint-py lint-docs fix-py fix-docs lint lints fix format check-dist check-types checks check test tests coverage show-version patch minor major dist dist-build dist-check test-dist publish upload docs serve notebooks css clean help

develop:  ## install development dependencies and library
	uv pip install -e '.[develop]'

requirements:  ## install prerequisite Python build requirements
	uv pip install -r pyproject.toml --extra develop

build:  ## build the Python library
	python -m build -n

install:  ## install library
	uv pip install .

lint-py:  ## lint Python with ruff
	python -m ruff check klink tests .github/scripts docs/source/conf.py
	python -m ruff format --check klink tests .github/scripts docs/source/conf.py

lint-docs:  ## lint contributor documentation
	python -m mdformat --check README.md docs/development.md
	python -m codespell_lib README.md docs/development.md

fix-py:  ## autoformat Python code
	python -m ruff check --fix klink tests .github/scripts docs/source/conf.py
	python -m ruff format klink tests .github/scripts docs/source/conf.py

fix-docs:  ## autoformat contributor documentation
	python -m mdformat README.md docs/development.md
	python -m codespell_lib --write README.md docs/development.md

lint: lint-py lint-docs  ## run all linters
lints: lint
fix: fix-py fix-docs  ## run all autoformatters
format: fix

check-dist:  ## check sdist and wheel contents
	check-dist -v --rebuild

check-types:  ## check Python types (advisory)
	ty check klink

checks: check-dist  ## run distribution checks
check: checks

test:  ## run Python tests
	python -m pytest tests

tests: test

coverage:  ## run tests with coverage
	python -m pytest tests --cov=klink --cov-report term-missing --cov-report xml

show-version:  ## show current library version
	@bump-my-version show current_version

patch:  ## bump a patch version
	@bump-my-version bump patch

minor:  ## bump a minor version
	@bump-my-version bump minor

major:  ## bump a major version
	@bump-my-version bump major

dist-build:  ## build Python distributions
	python -m build -w -s

dist-check:  ## check distribution metadata
	python -m twine check dist/*

dist:  ## build and check distributions
	$(MAKE) clean
	$(MAKE) dist-build
	$(MAKE) dist-check

publish: dist

upload: dist  ## upload distributions to PyPI manually
	python -m twine upload dist/* --skip-existing

test-dist:  ## test installed wheels and source distributions
	python .github/scripts/test-distributions.py

docs:  ## build the Sphinx theme demo
	python -m sphinx -W --keep-going -b html docs/source docs/build/html

serve:  ## serve built documentation on port 9090
	python -m http.server 9090 --directory docs/build/html

notebooks:  ## regenerate notebook exports (requires Pandoc)
	cd docs/source && python -c 'import klink; klink.convert_notebooks()'

css:  ## compile theme styles (requires lessc)
	lessc klink/less/klink.less klink/static/css/klink.css

clean:  ## remove distribution build output
	rm -rf build dist klink.egg-info

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "%-24s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
