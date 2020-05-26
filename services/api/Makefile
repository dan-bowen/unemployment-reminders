#
# Makefile for API service
#

.PHONY: help test lint clean

.DEFAULT_GOAL := help

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

test: ## Run unit tests
	@docker-compose exec api bash -c \
	    'FLASK_ENV="test" SECRET_KEY="" TWILIO_AUTH_TOKEN="" nose2 -v'

lint: ## Lint python files
	@docker-compose exec api bash -c \
	    'flake8'

clean: ## Clean python cache files
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
