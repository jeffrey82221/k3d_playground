VERSION_TAG="v0.0.11"
docker build -t test_kafka:${VERSION_TAG} .
docker tag test_kafka:${VERSION_TAG} localhost:6002/jeffrey82221/test_kafka:${VERSION_TAG}
docker push localhost:6002/jeffrey82221/test_kafka:${VERSION_TAG}
kubectl apply -f pod-consumer.yml
kubectl apply -f pod-producer.yml
sleep 10
kubectl logs -f test-consumer-pod