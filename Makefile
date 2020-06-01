#
# Makefile for Unemployment Reminders
#

.PHONY: help build start stop ssh-api

.DEFAULT_GOAL := help

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## (Re)build the containers
	@docker-compose build

start: ## Start the containers
	@docker-compose up

stop: ## Stop the containers
	@docker-compose down

ssh-api: ## SSH to the api container
	@docker-compose exec api bash

ngrok: ## API site over NGROK.
	@ngrok http -host-header=rewrite -subdomain=unemployment-reminders localhost:5000

migrate: ## Performe the initial migration
	@docker-compose exec api sls dynamodb migrate
