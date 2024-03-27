#!/bin/sh

echo "Stopping cluster..."
docker-compose down

echo "Cleaning unused images..."
docker image prune -af
