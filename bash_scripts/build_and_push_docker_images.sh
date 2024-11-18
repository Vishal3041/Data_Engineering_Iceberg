#!/bin/bash

# Exit script on any error
set -e

# Set your ECR repository names (make sure to create these repositories first)
SPARK_REPO="spark-repo"

# AWS ECR login
echo "Logging in to AWS ECR..."
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 767397764346.dkr.ecr.us-east-1.amazonaws.com

# Build Spark Docker image
echo "Building Spark Docker image..."
cd ../spark-docker/
docker build -t $SPARK_REPO .
docker tag $SPARK_REPO:latest 767397764346.dkr.ecr.us-east-1.amazonaws.com/$SPARK_REPO:latest

# Push Spark Docker image to ECR
echo "Pushing Spark Docker image to ECR..."
docker push 767397764346.dkr.ecr.us-east-1.amazonaws.com/$SPARK_REPO:latest

echo "Docker images pushed successfully."