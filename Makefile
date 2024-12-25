run:
	poetry run python main.py

test:
	poetry run pytest

lint:
	poetry run black .

build:
	poetry build
