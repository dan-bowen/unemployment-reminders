#
# Makefile for Unemployment Reminders
#

.PHONY: help test build

.DEFAULT_GOAL := help

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## (Re)build the containers.
	@docker-compose build

start: ## Start the containers.
	@docker-compose up && sls dynamodb migrate && sls dynamodb seed

seed: ## Seed Dynamo.
	@sls dynamodb migrate && sls dynamodb seed

stop: ## Stop the containers.
	@docker-compose down

test: ## Run unit tests.
	@docker-compose exec api bash -c \
	    'FLASK_ENV="test" SECRET_KEY="" TWILIO_ACCOUNT_SID="invalid" TWILIO_AUTH_TOKEN="invalid" DYNAMODB_ENDPOINT="http://localhost:8000" AWS_DEFAULT_REGION="us-east-1" nose2 -v'

coverage: ## Generate unit test code coverage report.
	@docker-compose exec api bash -c \
	    'FLASK_ENV="test" SECRET_KEY="" TWILIO_ACCOUNT_SID="invalid" TWILIO_AUTH_TOKEN="invalid" DYNAMODB_ENDPOINT="http://localhost:8000" AWS_DEFAULT_REGION="us-east-1" coverage run -m nose2 -v && coverage html'

lint: ## Lint python files.
	@docker-compose exec api bash -c \
	    'flake8 ./src'

clean: ## Clean python cache files.
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete

ssh-api: ## SSH to the api container.
	@docker-compose exec api bash

ngrok: ## API site over NGROK.
	@ngrok http -host-header=rewrite -subdomain=unemployment-reminders localhost:5000

invoke-poller: ## Invoke the Lambda poller function.
	@docker-compose exec api bash -c 'python-lambda-local -f lambda_handler src/poller.py data/poller.event.json'
