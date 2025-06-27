#!/bin/bash

# Login to ECR
aws ecr get-login-password --region eu-north-1 | \
docker login --username AWS --password-stdin 476114157013.dkr.ecr.eu-north-1.amazonaws.com

# Pull the latest image from ECR
docker pull 476114157013.dkr.ecr.eu-north-1.amazonaws.com/uber-demand:latest

if [ "$(docker ps -q -f name=uber-app)" ]; then
  docker stop uber-app
  docker rm uber-app
fi

docker run -d --name uber-app -p 80:8000 \
  -e DAGSHUB_USER_TOKEN=1675b557f5d0a7aaea12cf583d01eb0b90267d77 \
  476114157013.dkr.ecr.eu-north-1.amazonaws.com/uber-demand:latest
