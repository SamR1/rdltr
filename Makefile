include Makefile.config
-include Makefile.custom.config
.SILENT:

make-p:
	# Launch all P targets in parallel and exit as soon as one exits.
	set -m; (for p in $(P); do ($(MAKE) $$p || kill 0)& done; wait)

bandit:
	$(BANDIT) -r $(FLASK_APP) -c pyproject.toml

build-client:
	cd rdltr_front && $(NPM) run build

check-python: bandit lint-python type-check test

clean:
	rm -fr .pytest_cache
	rm -rf .mypy_cache

clean-all: clean
	rm -fr $(VENV)
	rm -fr .eggs
	rm -fr *.egg-info
	rm -fr rdltr_front/node_modules/
	rm -rf pip-wheel-metadata/
	rm -rf dist/
	rm -rf build/

fix-all: fix-python fix-front

fix-front:
	cd rdltr_front && $(NPM) lint --fix

fix-python:
	$(BLACK) $(FLASK_APP)

html:
	rm -rf docsrc/build
	rm -rf docs/*
	touch docs/.nojekyll
	$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	cp -a docsrc/build/html/. docs

install: install-python install-front

install-front:
	# NPM_ARGS="--ignore-engines", if errors with Node latest version
	cd rdltr_front && $(NPM) install --prod $(NPM_ARGS)

install-python:
	test -d $(VENV) || $(PYTHON_VERSION) -m venv $(VENV)
	$(PIP) install -U pip
	$(PIP) install -e .[test,doc]

lint-all: lint-python lint-front

lint-front:
	cd rdltr_front && $(NPM) lint

lint-python:
	$(PYTEST) --isort --black -m "isort or black" $(FLASK_APP)
	echo 'Running flake8...'
	$(FLAKE8) $(FLASK_APP)

lint-python-fix:
	$(BLACK) $(FLASK_APP)

migrate-db:
	$(FLASK) db migrate

run:
	echo 'Running on http://$(HOST):$(PORT)'
	cd rdltr && $(GUNICORN) -b $(HOST):$(PORT) "rdltr:create_app()" --error-logfile ../gunicorn-error.log

serve:
	$(MAKE) P="serve-python serve-front" make-p

serve-front:
	cd rdltr_front && $(NPM) serve

serve-python:
	echo 'Running on http://$(HOST):$(PORT)'
	$(FLASK) run --with-threads -h $(HOST) -p $(PORT)

test:
	$(PYTEST) $(FLASK_APP)/tests/tests --cov $(FLASK_APP) --cov-report term-missing $(PYTEST_ARGS)

test-ui:
	$(PYTEST) $(FLASK_APP)/tests/ui_tests --driver firefox $(PYTEST_ARGS)

type-check:
	echo 'Running mypy...'
	$(MYPY) $(FLASK_APP)

upgrade-db:
	$(FLASK) db upgrade
