#!/bin/sh

# Script will exit in case the curl fails
set -e

IP_ADDRESS=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps | grep $IMAGE_TAG | awk '{print $1}'))

curl -f http://$IP_ADDRESS:9000/
