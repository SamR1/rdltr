include Makefile.config
-include Makefile.custom.config
.SILENT:

clean:
	rm -fr $(VENV)
	rm -fr .eggs
	rm -fr *.egg-info
	rm -fr .pytest_cache

fix:
	$(ISORT) -rc $(FLASK_APP)
	black $(FLASK_APP)

install:
	test -d $(VENV) || virtualenv $(VENV) -p $(PYTHON_VERSION)
	$(PIP) install -e .[test]

serve:
	$(FLASK) run --with-threads -h $(HOST) -p $(PORT)

test:
	$(PYTHON) setup.py test
