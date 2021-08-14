SHELL=/bin/bash

down: 
	@docker-compose down;

up:
	@docker-compose up;

git:
	git add .
	git commit -m "$m"; 
	git add .
	git commit -m "$m";
	