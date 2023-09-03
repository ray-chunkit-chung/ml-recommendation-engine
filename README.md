# recommendation-engine

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

## Serve model

Serve locally

```bash
python src/serve.py
```

1. Containerize Your Model:

    Create a Docker container for your trained model. You'll need a Dockerfile that specifies the environment and dependencies required to run your model. This might include the machine learning framework (e.g., TensorFlow, PyTorch), any required libraries, and your Python code for serving the model as a REST API.

2. Build and Push the Docker Image:

    Build the Docker image using the Dockerfile.
Push the Docker image to a container registry like Docker Hub, Google Container Registry, or Amazon ECR. Make sure your Kubernetes cluster can access this registry.

3. Create Kubernetes Deployment:

    Write a Kubernetes Deployment YAML file that describes the desired state of your application. This file should include information about the Docker image to use, environment variables, and replicas.

4. Create Kubernetes Service:

    Write a Kubernetes Service YAML file to expose your application within the cluster. You can use a LoadBalancer, NodePort, or ClusterIP service type, depending on your requirements.

5. Deploy to Kubernetes:

    Apply the Deployment and Service YAML files to your Kubernetes cluster using kubectl apply.

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
