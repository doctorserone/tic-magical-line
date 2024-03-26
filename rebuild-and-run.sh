#!/bin/sh

echo "Stopping cluster..."
docker-compose down

echo "Cleaning unused images..."
docker image prune -af

echo "Rebuilding cluster..."
docker-compose build 

echo "Running cluster again..."
docker-compose up
