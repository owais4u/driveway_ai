.PHONY: help install test lint format clean docker-up docker-down

help:
	@echo "Drive-Thru Ordering System Development Commands:"
	@echo "install     - Install dependencies"
	@echo "test        - Run tests"
	@echo "lint        - Run code quality checks"
	@echo "format      - Format code"
	@echo "docker-up   - Start development environment"
	@echo "docker-down - Stop development environment"

install:
	pip install -r requirements/development.txt
	pre-commit install

test:
	pytest src/tests/ -v --cov=src/app --cov-report=html

lint:
	flake8 src/
	black --check src/
	isort --check-only src/
	mypy src/

format:
	black src/
	isort src/

docker-up:
	docker-compose up -d --build

docker-down:
	docker-compose down

migrate:
	alembic upgrade head

seed:
	python src/scripts/seed_database.py

logs:
	docker-compose logs -f drive-thru-app

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .coverage htmlcov .pytest_cache