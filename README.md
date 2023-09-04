# recommendation-engine

A minimal example of recommendation engine using Python, FastAPI, and TensorFlow. The model is trained on the MovieLens 100K dataset. Deployed to Kubernetes on AKS.

## Install packages

```bash
cd /tmp
wget https://www.python.org/ftp/python/3.11.5/Python-3.11.5.tgz
tar -xzvf Python-3.11.5.tgz
cd Python-3.11.5/
apt update
apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev libbz2-dev graphviz
./configure --enable-optimizations --enable-loadable-sqlite-extensions
make -j `nproc`
make altinstall
# ln -s /usr/local/bin/python3.11 /usr/local/bin/python
cd /com.docker.devenvironments.code
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade -r requirements.txt
```

## Train model

```bash
python src/train.py
```

## Predict

Predict the top 10 recommendations for user 1

```bash
python src/predict.py
```

## Serve model locally

Serve locally

```bash
python src/serve.py
```

## Serve locally with Docker

Build the Docker image using the Dockerfile. Push the Docker image to a container registry like Docker Hub, Google Container Registry, or Amazon ECR. Make sure your Kubernetes cluster can access this registry.

```bash
docker build -t raychung/recommendation-engine-serving-container .
docker run -p 5000:5000 raychung/recommendation-engine-serving-container
```

## Serve with Kubernetes

Write a Kubernetes Deployment YAML file that describes the desired state of your application. This file should include information about the Docker image to use, environment variables, and replicas.

Write a Kubernetes Service YAML file to expose your application within the cluster. You can use a LoadBalancer, NodePort, or ClusterIP service type, depending on your requirements.

If you want to expose your service to external users, consider using the LoadBalancer type, which can provision an external load balancer and allocate an external IP address for access.

### Install cli tools

Install azure cli

```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

Install kubectl

```bash
# x86-64 Download
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Validate the binary (optional)
curl -LO "https://dl.k8s.io/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check

# Install
install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
kubectl version --client
```

### Setup Azure Kubernetes Service (AKS) cluster

```bash
# Login Azure
az login --tenant $AZURE_TENANT_ID

# Create resource group
az group create --name $AZURE_RG --location $AZURE_LOCATION --subscription $AZURE_SUBSCRIPTION

# Create AKS cluster
az aks create --resource-group $AZURE_RG --name $AKS --subscription $AZURE_SUBSCRIPTION --node-count 3 --enable-addons monitoring --generate-ssh-keys

# Configure kubectl to use the credentials from the AKS cluster
az aks get-credentials --resource-group $AZURE_RG --subscription $AZURE_SUBSCRIPTION --name $AKS
```

### Deploy to Kubernetes

Apply the Deployment and Service YAML files to your Kubernetes cluster using kubectl apply.

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### Expose the service

Expose the service using a LoadBalancer type service. This will provision an external load balancer and allocate an external IP address for access.

```bash
kubectl expose deployment recommendation-engine-serving-deployment --type=LoadBalancer --name=recommendation-engine-loadbalancer --port=80 --target-port=5000
```

Once your service is exposed, you can access it using the public IP address of the Load Balancer.

```bash
kubectl get svc recommendation-engine-loadbalancer
```

There you go <http://EXTERNAL-IP/docs> to check out the API documentation.

### To save money when not in use

Scale the number of replicas down to 0 when you're not using the service. This will stop the service and deallocate the VMs, saving you money.

```bash
az aks scale --resource-group $AZURE_RG --subscription $AZURE_SUBSCRIPTION --name $AKS --node-count 1
```

or just delete the service and deployment

```bash
kubectl delete service your-service-name
kubectl delete deployment your-deployment-name
```

```bash
kubectl get services  # This should not show your service anymore
kubectl get deployments  # This should not show your deployment anymore
```

## Other Considerations

6. Scale and Monitor:

    Use Kubernetes commands to scale the number of replicas up or down based on your application's needs.
    Implement monitoring and logging solutions to track the performance and health of your application.

7. Ingress Controller (Optional):

    If you want to expose your API to external users, consider using an Ingress Controller to manage external access and routing to your service.

8. Set Up Autoscaling (Optional):

    Configure Horizontal Pod Autoscaling (HPA) based on metrics like CPU or custom metrics to automatically adjust the number of replicas based on demand.

9. Secure Your API:

    Implement authentication and authorization mechanisms to secure your REST API. Kubernetes provides tools like Kubernetes Service Accounts and Role-Based Access Control (RBAC) for this purpose.

10. Continuous Integration/Continuous Deployment (CI/CD):

    Implement CI/CD pipelines to automate the process of building and deploying your model to Kubernetes whenever you make changes to your code or model.

11. Testing and Validation:

    Thoroughly test your deployed REST API to ensure it's functioning as expected in the Kubernetes cluster.

12. Monitoring and Logging:

    Set up monitoring and logging solutions to keep track of the health and performance of your deployed model. Kubernetes has integrations with tools like Prometheus and Grafana.

13. Maintenance and Updates:

    Regularly update and maintain your deployed application, including updates to the model, dependencies, and the container image.

14. Rolling Updates and Rollbacks:

    Implement strategies for rolling updates and rollbacks in Kubernetes to minimize downtime and risk during updates.

15. Documentation:

    Document how to use your REST API, including API endpoints, input/output formats, and authentication details.

## References

<https://towardsdatascience.com/recommender-systems-from-learned-embeddings-f1d12288f278>

<https://towardsdatascience.com/introduction-to-embedding-based-recommender-systems-956faceb1919>
