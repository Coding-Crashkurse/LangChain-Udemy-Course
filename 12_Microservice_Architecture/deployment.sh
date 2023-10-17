#!/bin/bash

# Function to execute Docker operations
do_docker() {
    # Check if the registry is already running
    if [ -z "$(docker ps -q -f name=local-registry)" ]; then
        if [ -n "$(docker ps -aq -f status=exited -f name=local-registry)" ]; then
            # cleanup
            echo "Removing exited local registry container..."
            docker rm local-registry
        fi
        # run container
        echo "Starting Docker Registry..."
        docker run -d -p 5000:5000 --name local-registry registry:2
    else
        echo "Docker Registry is already running..."
    fi

    echo "Building images..."
    # Adjust these paths if your Dockerfile locations have changed
    docker build -t mypostgres ./postgres
    docker build -t myconversation_service ./conversation_service
    docker build -t myai_service ./ai_service
    docker build -t myfrontend_italian ./frontend_italian
    docker build -t myfrontend_korean ./frontend_korean

    echo "Tagging and pushing images..."
    # For Postgres
    docker tag mypostgres localhost:5000/mypostgres
    docker push localhost:5000/mypostgres

    # For Conversation Service
    docker tag myconversation_service localhost:5000/myconversation_service
    docker push localhost:5000/myconversation_service

    # For AI Service
    docker tag myai_service localhost:5000/myai_service
    docker push localhost:5000/myai_service

    # For Frontend Italian
    docker tag myfrontend_italian localhost:5000/myfrontend_italian
    docker push localhost:5000/myfrontend_italian

    # For Frontend Korean
    docker tag myfrontend_korean localhost:5000/myfrontend_korean
    docker push localhost:5000/myfrontend_korean
}

# Function to execute Kubernetes operations
do_kubernetes() {
    echo "Deploying to Kubernetes..."
    kubectl apply -f local-deployment.yaml
    kubectl apply -f local_ingress.yaml
}

# Main logic of the script
if [ "$1" == "--build" ]; then
    do_docker
    do_kubernetes
else
    do_kubernetes
fi
