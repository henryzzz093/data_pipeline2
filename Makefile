SHELL=/bin/bash

down: 
	@docker-compose down;

format:
	@python -m black dags data_pipelines
	@python -m flake8 dags data_pipelines

.ONESHELL:
install:
	@rm -rf .venv;
	@python -m venv .venv;
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

run-app:
	@tput setaf 2;
	@echo installing application;
	@tput sgr0;
	@make install; 
	@tput setaf 2;
	@echo application successfully installed!
	@echo launching application!
	@tput sgr0;
	@docker-compose up -d; 



reset:
	@rm -rf venv;
	@docker-compose down;
	@docker-compose rm -f;
<<<<<<< HEAD
	@docker image prune -af;

update:
	@export PATH="/usr/local/opt/make/libexec/gnubin:$PATH"
=======
>>>>>>> 70bc09e76e06b94fc4c163d00737308ee06a7c6d
	

up:
	@docker-compose up;




	