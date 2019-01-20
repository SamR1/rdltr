include Makefile.config
-include Makefile.custom.config
.SILENT:

make-p:
	# Launch all P targets in parallel and exit as soon as one exits.
	set -m; (for p in $(P); do ($(MAKE) $$p || kill 0)& done; wait)

build:
	cd rdltr_front && $(NPM) run build

clean:
	rm -fr $(VENV)
	rm -fr .eggs
	rm -fr *.egg-info
	rm -fr .pytest_cache
	rm -fr rdltr_front/node_modules/
	rm -fr rdltr/dist/

fix:
	$(ISORT) -rc $(FLASK_APP)
	black $(FLASK_APP)

install: install-python install-front

install-front:
	cd rdltr_front && $(NPM) install

install-python:
	test -d $(VENV) || virtualenv $(VENV) -p $(PYTHON_VERSION)
	$(PIP) install -e .[test]

migrate-db:
	$(FLASK) db migrate

serve:
	$(MAKE) P="serve-python serve-front" make-p

serve-front:
	cd rdltr_front && $(NPM) run dev

serve-python: build
	$(FLASK) run --with-threads -h $(HOST) -p $(PORT)

test:
	$(PYTEST) $(FLASK_APP) $(PYTEST_ARGS)

upgrade-db:
	$(FLASK) db upgrade
