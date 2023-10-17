#!/bin/bash

# Function to remove Kubernetes deployments and services
force_remove_kubernetes_objects() {
    echo "Forcefully removing Kubernetes pods..."
    kubectl delete pods --force --grace-period=0 frontend-557f997449-qjgdr service2-75595c88b7-z7cfh service3-784c95b9f-6bxvp

    echo "Attempting to remove Kubernetes deployments, services, and ingress again..."
    kubectl delete -f local-deployment.yaml
    kubectl delete -f local_ingress.yaml
}

# Function to stop and remove Docker images and containers
remove_docker_objects() {
    echo "Stopping local Docker Registry if it's running..."
    if [ -n "$(docker ps -q -f name=local-registry)" ]; then
        docker stop local-registry
        docker rm local-registry
    fi

    echo "Removing Docker images..."
    docker rmi localhost:5000/mypostgres
    docker rmi localhost:5000/myconversation_service
    docker rmi localhost:5000/myai_service
    docker rmi localhost:5000/myfrontend_italian
    docker rmi localhost:5000/myfrontend_korean
}

# Main logic of the script
if [ "$1" == "--full" ]; then
    force_remove_kubernetes_objects
    remove_docker_objects
else
    force_remove_kubernetes_objects
fi
