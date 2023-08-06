PROJECT_NAME = django_logger
SHELL := /bin/sh
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  all                      to setup the whole development environment for the project"
	@echo "  env                      to create the virtualenv for the project"
	@echo "  setup_dev                install the requirements to the virtualenv"
	@echo "  migrations               create new migrations"
	@echo "  migrate                  update database with latest changes"
	@echo "  run_dev                  start the development server"
	@echo "  docs                  compile documentation"
	@echo "  clean                  clean environment"

HERE = $(shell pwd)
VENV = $(HERE)/venv
BIN = $(VENV)/bin
PYTHON = $(BIN)/python3
VIRTUALENV = python3 -m venv
MAKE = make

.PHONY: all test docs

dev: all setup_dev migrate

all: clean env

env:
	$(VIRTUALENV) $(VENV)

clean:
	rm -rf $(VENV)
	rm -rf build
	rm -rf dist
	find . -name "*.pyc" -exec rm -rf {} \;

test_dependencies:
	$(BIN)/pip3 install -e ".[tests]"

test: test_dependencies
	$(BIN)/tox

docs_depedencies:
	$(BIN)/pip3 install -e ".[docs]"

docs: docs_depedencies
	cd docs && $(MAKE) html SPHINXBUILD=$(VENV)/bin/sphinx-build

run_dev: setup_dev
	$(PYTHON) django_logger_project/manage.py

setup_dev:
	$(BIN)/pip3 install -e ".[dev]"

migrations:
	$(PYTHON) makemigrations.py

migrate:
	$(PYTHON) migrate.py

twine:
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel
	$(BIN)/twine upload dist/*