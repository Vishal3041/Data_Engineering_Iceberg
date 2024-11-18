#!/bin/bash

# Exit script on any error
set -e

# Add the Kubeflow Spark Operator Helm repository
echo "Adding the Kubeflow Spark Operator Helm repository..."
helm repo add spark-operator https://kubeflow.github.io/spark-operator
helm repo update

# Install the Spark Operator into the spark-operator namespace
echo "Installing Spark Operator..."
helm install spark-operator spark-operator/spark-operator \
    --namespace spark-operator --create-namespace --wait

# Apply an example Spark application (SparkPi)
echo "Applying the SparkPi example application..."
kubectl apply -f https://raw.githubusercontent.com/kubeflow/spark-operator/refs/heads/master/examples/spark-pi.yaml

# Wait for the application to complete
echo "Checking the status of the Spark application..."
kubectl get sparkapp spark-pi

echo "Spark Operator and SparkPi example deployed successfully."