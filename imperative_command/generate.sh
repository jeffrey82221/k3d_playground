kubectl run nginx --image=nginx --dry-run=client -o yaml > nginx-pod.yaml
kubectl create deployment --image=nginx nginx --dry-run=client -o yaml > nginx-deployment.yaml
kubectl create deployment --image=nginx nginx --replicas=4 --dry-run=client -o yaml > nginx-deployment-4.yaml
kubectl create service clusterip redis --tcp=6379:6379 --dry-run=client -o yaml > redis-service-2.yaml