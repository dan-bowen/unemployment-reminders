# Quickstart for local development

## Prerequisites

- docker desktop
- docker compose
- aws cli

You'll need a Twilio account as well as an Autopilot chatbot configured.

## Application Setup

1. Rename `.env.dist` to `.env` and enter your values.
1. Rename `serverless.dist.yml` to `serverless.yml` and enter your values.
1. Run `make start` to start the containers.
1. Run `make help` to explore other commands.

# Deployments

Deployments are done via the [Serverless Framework](https://www.serverless.com/). With 
containers running execute the following commands:

1. SSH to the API container

    ```
    $ make ssh-api
    ```

1. Within the container, deploy with Serverless

    ```
    $ sls login
    $ sls deploy --aws-s3-accelerate
    ```