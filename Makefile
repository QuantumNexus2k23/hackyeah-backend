.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT


define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

COMMIT_SHA := $(shell git rev-parse HEAD)
BRANCH_NAME := $(shell git rev-parse --abbrev-ref HEAD)
TAGS := -t $(DOCKER_REGISTRY):$(COMMIT_SHA) -t $(DOCKER_REGISTRY):$(BRANCH_NAME)

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -f coverage.xml
	rm -fr htmlcov/
	rm -fr .pytest_cache

test: ## run tests quickly with the default Python
	pytest hackyeah

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	pytest --cov=hackyeah hackyeah
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

quality-check: ## check quality of code
	black --check hackyeah
	isort --check hackyeah
	flake8 hackyeah
	mypy hackyeah

autoformatters: ## runs auto formatters
	black hackyeah
	isort hackyeah

_install_pip_tools:
	python -m piptools > /dev/null 2>&1 || pip install pip-tools

pip-compile: _install_pip_tools
	ls requirements/*.in | xargs -n 1 pip-compile

install_requirements: _install_pip_tools  ## install python requirements
	pip install -r requirements/dev.txt

bootstrap: install_requirements  ## bootstrap project
	python manage.py migrate
	[ -d fixtures ] && python manage.py loaddata fixtures/*.yaml || exit 0

rebuild-db:  ## recreates database with fixtures
	echo yes | python manage.py reset_db
	python manage.py migrate
	python manage.py loaddata fixtures/*

bootstrap-docker:  ## bootstrap project in docker
	docker-compose up --build -d
	docker-compose exec web python manage.py migrate
	docker-compose exec web python manage.py loaddata fixtures/*.yaml

show-docker-tags: ## shows docker tags for building and pushing image
	echo $(TAGS)

docker-build:  ## build docker image
	docker build $(TAGS) .

docker-push:
	docker push $(DOCKER_REGISTRY):$(COMMIT_SHA)
	docker push $(DOCKER_REGISTRY):$(BRANCH_NAME)
