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
	pip install -e .;\
	poetry install; \
	poetry run pre-commit install; \

run-app:
	make install; \
	docker-compose up -d; \

reset:
	@rm -rf venv;
	@docker-compose down;
	@docker-compose rm -f;
	@docker image prune -af;
	

up:
	@docker-compose up;




	