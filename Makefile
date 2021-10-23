SHELL=/bin/bash

down: 
	@docker-compose down;

format:
	@python -m black dags data_pipelines
	@python -m flake8 dags data_pipelines

.ONESHELL:
install:
	@python3 -m venv .venv;
	@tput setaf 2;
	@echo "Activating virtual environment";
	@tput sgr0;
	@poetry shell;
	@pip install --upgrade pip;
	@tput setaf 2;
	@echo "Installing packages";
	@tput sgr0;
	@poetry install;
	@poetry run pre-commit install;
	@tput setaf 2;
	@echo "Installation complete! :)";
	@tput sgr0;

run-app-dev:
	@tput setaf 2;
	@echo "Initializing environment";
	@tput sgr0;
	@make reset;
	@tput setaf 2;
	@echo Installing application;
	@tput sgr0;
	@make install; 
	@tput setaf 2;
	@echo Application successfully installed!
	@echo Launching application!
	@tput sgr0;
	@docker-compose up; 

run-app:
	@tput setaf 2;
	@echo Launching application!
	@tput sgr0;
	@docker-compose up;


reset:
	@rm -rf .venv;
	@docker-compose down;
	@docker-compose rm -f;
	

up:
	@docker-compose up;




	