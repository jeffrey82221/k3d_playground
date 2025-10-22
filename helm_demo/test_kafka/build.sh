VERSION_TAG="v0.0.7"
docker build -t test_hello:${VERSION_TAG} .
docker tag test_hello:${VERSION_TAG} localhost:6002/jeffrey82221/test_hello:${VERSION_TAG}
docker push localhost:6002/jeffrey82221/test_hello:${VERSION_TAG}
kubectl delete pod test-pod
kubectl create -f pod-definition.yml


kubectl get pods shows:

kafka-1-controller-0   0/1     Init:ImagePullBackOff   0             35m
kafka-1-controller-1   0/1     Init:ImagePullBackOff   0             35m
kafka-1-controller-2   0/1     Init:ImagePullBackOff   0             35m
test-pod               0/1     CrashLoopBackOff        3 (14s ago)   66s

How to get the bootstrap servers for kafka cluster?

I want to connect to the server within the k8s cluster.