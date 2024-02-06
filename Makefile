TMPREPO=/tmp/docs/klink

.PHONY: clean css docs serve pages dist develop lint fix

develop:
	python -m pip install -e .[dev]
	python -m pip install nbconvert

lint:
	python -m ruff klink setup.py docs/source/conf.py

fix:
	python -m ruff format klink setup.py docs/source/conf.py

clean:
	- rm -rf build
	- rm -rf dist
	- rm -rf klink.egg-info

css:
	lessc klink/less/klink.less klink/static/css/klink.css
	- cp klink/static/css/klink.css docs/build/html/_static/css/klink.css

docs: css
	$(MAKE) -C docs/ clean
	$(MAKE) -C docs/ html 

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
	python setup.py sdist upload
