.PHONY: build install-packages test style bumpver bucket docker clean

install:
	pip3 install -U pip
	pip3 install poetry==1.8.3
	pip3 install virtualenv==20.30.0
	poetry config virtualenvs.create false
	poetry install --no-interaction --no-ansi --with dev --with optional --verbose

build:
	poetry build -f wheel


# Utilities
style:
	poetry run black iterlike_dataset

type: 
	poetry run mypy iterlike_dataset --config-file pyproject.toml




