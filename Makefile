run:
	python src/main.py

lint:
	isort src && flake8 src

test:
# 	pytest src --ignore=src/tests/integration/
	pytest src

cov:
	pytest src --cov=src
