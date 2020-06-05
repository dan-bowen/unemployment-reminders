#!/bin/bash
set -e

sls dynamodb migrate

flask run --host=0.0.0.0
