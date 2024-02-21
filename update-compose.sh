#!/bin/bash

# Get MongoDB URL from user
read -p "MongoDB URL: " mongo_url

# Get JWT Secret Key from user
read -p "JWT Secret Key: " jwt_secret_key

# Update the Docker Compose file
sed -i'' -e "s|^\(\s*-\s*MONGO_URL=\).*|\1${mongo_url//&/\\&}|" docker-compose.yml
sed -i'' -e "s|^\(\s*-\s*JWT_SECRET_KEY=\).*|\1${jwt_secret_key}|" docker-compose.yml

echo "Added MongoDB URL and JWT Secret Key."

# Start services with Docker Compose
docker-compose up --build
