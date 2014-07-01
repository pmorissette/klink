.PHONY: clean css docs serve

clean:
	- rm -rf build
	- rm -rf dist
	- rm -rf klink.egg-info

css:
	lessc --clean-css klink/less/klink.less klink/static/css/klink.css
	- cp klink/static/css/klink.css docs/build/html/_static/css/klink.css

docs: css
	$(MAKE) -C docs/ clean
	$(MAKE) -C docs/ html 

serve:
	cd docs/build/html; \
	python -m SimpleHTTPServer 9090
