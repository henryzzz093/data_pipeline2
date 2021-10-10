SHELL=/bin/bash

down: 
	@docker-compose down;

format:
	@python -m black dags data_pipelines
	@python -m flake8 dags data_pipelines

install:
	@python -m venv venv;
	\
	source venv/bin/activate; \
	pip install --upgrade pip; \
	pip install -e .\

reset:
	@rm -rf venv;
	@echo "venv folder deleted"

up:
	@docker-compose up;




	