.PHONY: help install dev test lint clean build deploy

help:
	@echo "Available commands:"
	@echo "  install     Install dependencies"
	@echo "  dev         Start development server"
	@echo "  test        Run tests"
	@echo "  lint        Run linting"
	@echo "  clean       Clean up generated files"
	@echo "  build       Build Docker image"
	@echo "  deploy      Deploy to production"

install:
	pip install -r requirements.txt
	alembic upgrade head

dev:
	python scripts/start_dev.py

test:
	python scripts/run_tests.py

lint:
	black app/ tests/
	isort app/ tests/
	flake8 app/ tests/

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .coverage htmlcov/ .pytest_cache/

build:
	docker build -t taskmanager-fastapi .

deploy:
	docker-compose -f docker-compose.yml up -d --build

init-db:
	python scripts/init_db.py

migrate:
	alembic upgrade head

new-migration:
	alembic revision --autogenerate -m "$(message)"
