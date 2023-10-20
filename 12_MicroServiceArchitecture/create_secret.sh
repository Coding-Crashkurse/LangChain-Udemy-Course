#!/bin/bash

kubectl create secret generic openai-secret --from-literal=OPENAI_API_KEY=sk-...
kubectl create secret generic postgres-password --from-literal=POSTGRES_PASSWORD='your-secret-password'