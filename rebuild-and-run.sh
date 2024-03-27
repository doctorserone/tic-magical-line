#!/bin/sh

echo "Rebuilding cluster..."
docker-compose build 

echo "Running cluster again..."
docker-compose up
