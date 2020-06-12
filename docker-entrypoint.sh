#!/bin/bash
set -e

sls dynamodb migrate
sls dynamodb seed --seed=init

flask run --host=0.0.0.0
