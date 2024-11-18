#!/bin/bash

# Exit script on any error
set -e

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Docker is not installed, installing Docker..."
    sudo apt-get update
    sudo apt-get install -y docker.io
else
    echo "Docker is already installed."
fi

# Check if Helm is installed
if ! command -v helm &> /dev/null
then
    echo "Helm is not installed, installing Helm..."
    curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
else
    echo "Helm is already installed."
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null
then
    echo "kubectl is not installed, installing kubectl..."
    curl -LO "https://dl.k8s.io/release/v1.21.0/bin/linux/amd64/kubectl"
    chmod +x ./kubectl
    sudo mv ./kubectl /usr/local/bin/kubectl
else
    echo "kubectl is already installed."
fi

# Ensure AWS CLI is installed
if ! command -v aws &> /dev/null
then
    echo "AWS CLI is not installed, installing AWS CLI..."
    sudo apt-get install awscli -y
else
    echo "AWS CLI is already installed."
fi

echo "Prerequisites installed successfully."