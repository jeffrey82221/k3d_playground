VERSION_TAG="v0.0.8"
docker build -t test_hello:${VERSION_TAG} .
docker tag test_hello:${VERSION_TAG} localhost:6002/jeffrey82221/test_hello:${VERSION_TAG}
docker push localhost:6002/jeffrey82221/test_hello:${VERSION_TAG}
kubectl delete pod test-pod
kubectl apply -f pod-definition.yml
sleep 10
kubectl logs -f test-pod