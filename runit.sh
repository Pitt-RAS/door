#!/bin/sh

docker build -t door .
docker stop door
docker rm door
docker run --name=door --net=host --privileged=true --restart=always -e SLACK_API_TOKEN="PUT_TOKEN_HERE" -v /database.txt:/app/database.txt door
