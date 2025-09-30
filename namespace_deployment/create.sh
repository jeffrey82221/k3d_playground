kubectl create namespace dev
kubectl create -f deployment-definition.yaml
kubectl get deployments --namespace=dev
kubectl get replicaset --namespace=dev
kubectl get pods --namespace=dev