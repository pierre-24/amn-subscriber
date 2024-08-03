install:
	pip install -e .

install-dev:
	pip install -e .[dev]

init:
	flask --app amn_subscriber init

lint:
	flake8 amn_subscriber tests --max-line-length=120 --ignore=N802

test:
	python -m unittest discover -s tests

run:
	flask --app amn_subscriber run