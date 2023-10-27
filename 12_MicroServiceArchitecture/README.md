# Restaurant Chatbot Project

This project introduces an advanced restaurant chatbot distributed across multiple microservices. The chatbot is designed to handle a variety of inquiries about the restaurant, such as operating hours, menu choices, and health and safety measures, thereby improving customer interaction and service.

## Services

The architecture encompasses the following microservices:

1. **Frontend:** This React application provides a user-friendly interface, facilitating seamless interaction with the chatbot.

2. **Service2:** Built with Python (FastAPI), this backend service serves as the communication bridge between the frontend and Service3, handling the chat history between the user and the chatbot.

3. **Service3:** Another Python (FastAPI) application, this service contains the chatbot algorithm and liaises with the AI engine (OpenAI GPT-3.5-turbo) to interpret user inquiries and formulate appropriate responses.

4. **Redis:** Employed for state storage, this Redis server ensures data consistency across services.

5. **Postgres:** This Postgres server is responsible for storing vector embeddings and other relevant data structures.

## Setup

Outlined as a microservice architecture blueprint, this setup can be deployed on a single machine, with potential scalability to larger on-premises clusters or extensive cloud services such as AWS, Google Cloud, or Microsoft Azure. Follow these steps for configuration:

1. **Docker Desktop:** Docker Desktop, compatible with Windows, Mac, and Linux, enables the establishment of a single-machine Kubernetes cluster. It can be downloaded from [Docker Desktop](https://www.docker.com/products/docker-desktop/).

2. **Kubernetes Ingress Controller:** Since this component isn't included in the standard Docker Desktop installation, it needs to be installed separately:

   ```shell
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
   ```

   Initiate by safeguarding necessary passwords and your OpenAI API key as a secret. Amend the values in `secrets.yaml` and run `kubectl apply -f secrets.yaml`.

   Kubernetes necessitates an image registry from which to pull images. Create one on your machine, then build your images, tag them, and push them into your registry. Subsequently, you can orchestrate your Deployments, Services, ConfigMaps, and Ingress using the convenience script `deployment.sh`. Run `bash deployment.sh` for comprehensive setup.

3. **Verifying Service Status:**

   Inspect the status of your applications with `kubectl get pods`. The expected output:

   | NAME                      | READY | STATUS  | RESTARTS | AGE |
   | ------------------------- | ----- | ------- | -------- | --- |
   | frontend-557f997449-d7dm5 | 1/1   | Running | 0        | 22h |
   | postgres-cf568b9dd-j4pz2  | 1/1   | Running | 0        | 22h |
   | redis-5f5b7bb696-82z8p    | 1/1   | Running | 0        | 22h |
   | service2-75595c88b7-cghxg | 1/1   | Running | 0        | 22h |
   | service3-599b6cc64-2pjpm  | 1/1   | Running | 0        | 22h |

   If there are deviations, diagnose issues within specific pods with commands like `kubectl logs service2-75595c88b7-cghxg`.

4. **Terminating Services:**

   To dismantle your setup, execute: `kubectl delete -f all-deployments.yaml`.

## Data Population

Utilize `insert_data.py` to populate your Postgres database with initial data. Once the services are operational, execute the script, which connects to the Postgres service, creates necessary tables, and populates them with data.
