# Quickstart for local development

## Prerequisites

- docker desktop
- `docker-compose`
- node.js
- aws cli

You'll need a Twilio account as well as an Autopilot chatbot configured.

## Application Setup

```shell

# Copy the env file and enter your values
cp .env.dist .env
vi .env


# Copy serverless file and enter your values
cp serverless.dist.yml serverless.yml
vi serverless.yml


# Set up Node
npm install -g serverless
npm install

# Start the containers
make start

# Migrations
make seed

# Explore other Make commands
make help
```

# Deployments

Deployments are done via the [Serverless Framework](https://www.serverless.com/).

```shell
# If you're using the Dashboard. Otherwise just deploy
sls login
sls deploy --aws-s3-accelerate
```