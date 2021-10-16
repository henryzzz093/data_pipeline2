SHELL=/bin/bash

down: 
	@docker-compose down;

format:
	@python -m black dags data_pipelines
	@python -m flake8 dags data_pipelines

.ONESHELL:
install:
	@rm -rf venv;
	@python -m venv venv;
	@tput setaf 2;
	@echo "Activating virtual environment";
	@tput sgr0;
	@source venv/bin/activate;
	@tput setaf 2;
	@echo "Installing packages";
	@tput sgr0;
	@pip install --upgrade pip;
	@pip install -e .;
	@poetry install;
	@poetry run pre-commit install;
	@tput setaf 2;
	@echo "Installation complete! :)";
	@tput sgr0;

run-app:
	make install; \
	docker-compose up -d; \



reset:
	@rm -rf venv;
	@docker-compose down;
	@docker-compose rm -f;
	@docker image prune -af;

update:
	@export PATH="/usr/local/opt/make/libexec/gnubin:$PATH"
	

up:
	@docker-compose up;




	