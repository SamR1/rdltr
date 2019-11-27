include Makefile.config
-include Makefile.custom.config
.SILENT:

make-p:
	# Launch all P targets in parallel and exit as soon as one exits.
	set -m; (for p in $(P); do ($(MAKE) $$p || kill 0)& done; wait)

build-client:
	cd rdltr_front && $(NPM) run build

clean:
	rm -fr $(VENV)
	rm -fr .eggs
	rm -fr *.egg-info
	rm -fr .pytest_cache
	rm -fr rdltr_front/node_modules/
	rm -rf pip-wheel-metadata/
	rm -rf dist/
	rm -rf build/

fix-all: fix-python fix-front

fix-front:
	cd rdltr_front && $(NPM) lint --fix

fix-python:
	black $(FLASK_APP)

install: install-python install-front

install-front:
	cd rdltr_front && $(NPM) install

install-python:
	test -d $(VENV) || virtualenv $(VENV) -p $(PYTHON_VERSION)
	$(PIP) install -e .[test]

lint-all: lint-python lint-front

lint-front:
	cd rdltr_front && $(NPM) lint

lint-python:
	$(PYTEST) --flake8 --isort -m "flake8 or isort" $(FLASK_APP)

migrate-db:
	$(FLASK) db migrate

run:
	cd rdltr && $(GUNICORN) -b 127.0.0.1:5000 "rdltr:create_app()" --error-logfile ../gunicorn-error.log

serve:
	$(MAKE) P="serve-python serve-front" make-p

serve-front:
	cd rdltr_front && $(NPM) serve

serve-python:
	$(FLASK) run --with-threads -h $(HOST) -p $(PORT)

test:
	$(PYTEST) $(FLASK_APP)/tests/tests --cov $(FLASK_APP) --cov-report term-missing $(PYTEST_ARGS)

test-ui:
	$(PYTEST) $(FLASK_APP)/tests/ui_tests --driver firefox $(PYTEST_ARGS)

upgrade-db:
	$(FLASK) db upgrade
