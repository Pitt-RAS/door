#!/bin/sh

docker build -t door .
docker stop door
docker rm door
docker run --name=door --net=host --privileged=true --restart=always -d -e SLACK_API_TOKEN="SLACK_KEY_HERE" -v /database.txt:/app/door/door/database.txt door
