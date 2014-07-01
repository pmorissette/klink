.PHONY: css serve


css:
	lessc --clean-css klink/less/klink.less klink/static/css/klink.css
	- cp klink/static/css/klink.css docs/build/html/_static/css/klink.css

docs: css
	$(MAKE) -C docs/ clean
	$(MAKE) -C docs/ html 

serve:
	cd docs/build/html; \
	python -m SimpleHTTPServer 9090
