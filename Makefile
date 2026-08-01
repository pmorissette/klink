TMPREPO=/tmp/docs/klink

.PHONY: clean css docs serve pages dist upload develop lint fix

develop:
	python -m pip install -e .[dev]

lint:
	python -m ruff check klink docs/source/conf.py
	python -m ruff format --check klink docs/source/conf.py

fix:
	python -m ruff check --fix klink docs/source/conf.py
	python -m ruff format klink docs/source/conf.py

clean:
	rm -rf build dist klink.egg-info

css:
	lessc klink/less/klink.less klink/static/css/klink.css
	cp klink/static/css/klink.css docs/build/html/_static/css/klink.css

docs: 
	$(MAKE) -C docs/ clean
	$(MAKE) -C docs/ html SPHINXOPTS="-W --keep-going"

serve:
	cd docs/build/html; \
	python -m http.server 9090

pages:
	- rm -rf $(TMPREPO)
	git clone -b gh-pages git@github.com:pmorissette/klink.git $(TMPREPO)
	rm -rf $(TMPREPO)/*
	cp -r docs/build/html/* $(TMPREPO)
	cd $(TMPREPO); \
	git add -A ; \
	git commit -a -m 'auto-updating docs' ; \
	git push

dist:
	python -m build -s -w
	python -m twine check dist/*

upload: clean dist
	python -m twine upload dist/* --skip-existing
