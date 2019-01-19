include Makefile.config
-include Makefile.custom.config
.SILENT:

clean:
	rm -fr $(VENV)
	rm -fr *.egg-info

install:
	test -d $(VENV) || virtualenv $(VENV) -p $(PYTHON_VERSION)
	$(PIP) install -e .[test]

serve:
	$(FLASK) run --with-threads -h $(HOST) -p $(PORT)

test:
	$(PYTHON) setup.py test

test-python-xml:
	$(PYTEST) --flake8 --isort --cov rdltr --cov-report xml

update-cov:	test-python-xml
	$(COV) -r coverage.xml
