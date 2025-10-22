# 如何達到 Producer 的測試？

## 0. 架設 kafka 於 k8s 

```
helm uninstall kafka-1
helm repo add kafka-repo https://helm-charts.itboon.top/kafka
helm repo update kafka-repo
helm pull --untar kafka-repo/kafka
helm install kafka-1 ./kafka
```

>>

```
NAME: kafka-1
LAST DEPLOYED: Wed Oct 22 22:25:55 2025
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
>>> bootstrap-servers:
    kafka-1-broker-0.kafka-1-headless.default.svc.cluster.local:9092
```

### Advance: 

#### One controller and one broker

```
helm upgrade --install kafka \
  --namespace kafka-demo \
  --create-namespace \
  --set broker.persistence.size="20Gi" \
  kafka-repo/kafka
```

#### Deploy a highly available cluster

```
 helm upgrade --install kafka \
  --namespace kafka-demo \
  --create-namespace \
  --set controller.replicaCount="3" \
  --set broker.replicaCount="3" \
  --set broker.heapOpts="-Xms4096m -Xmx4096m" \
  --set broker.resources.requests.memory="8Gi" \
  --set broker.resources.limits.memory="16Gi" \
  kafka-repo/kafka
```

#### Using LoadBalancer


```
helm upgrade --install kafka \
  --namespace kafka-demo \
  --create-namespace \
  --set broker.external.enabled="true" \
  --set broker.external.service.type="LoadBalancer" \
  --set broker.external.domainSuffix="kafka.example.com" \
  kafka-repo/kafka
```


## 1. 學會一個 python 執行檔的打包與部屬 

1. 建立 print hello word  python script 

see `test.py`

2. 安裝 綁定 k3d 的 image registry 

```bash
k3d cluster create mycluster --registry-create mycluster-registry:6002
docker ps -f name=mycluster-registry
```

3. 將 k3d 連結到 local registry: 

```bash
docker network connect k3d-k3s-default registry
```

4. 將 python script 與 requirements.txt 的安裝包進 image 中，放上 image registry 

```bash
docker login localhost:6002
>> username: jeffrey82221
>> password: xxx 
docker build -t test_hello:v0.0.4 .
docker tag test_hello:v0.0.4 localhost:6002/jeffrey82221/test_hello:v0.0.4
docker push localhost:6002/jeffrey82221/test_hello:v0.0.4
```

Or 

```bash
chmod 777 build.sh
. build.sh
```

Check pushed image:

```
curl http://localhost:6002/v2/_catalog
```
>> `{"repositories":["jeffrey82221/test_hello","ubuntu"]}`


5. 將此 image 的 pull 與 run 用 deployment yaml 起起來

```
kubectl create -f pod-definition.yml
kubectl get pods
kubectl logs --timestamps -f test-pod
kubectl delete pod test-pod
```

## 2. 學會將此 image 的 logs 寫出來到一個 volumn 裡面

1. Dockerfile python 執行時納入 -u (unbuffer)，讓 log 可以即時呈現

```
CMD ["python", "-u", "test.py"]
```

2. kubectl 加入 --timestamps 和 -f (即時呈現logs)

```
kubectl logs --timestamps -f test-pod
```

## 3. 將此 python script 改成 producer 的資料寫入


1. 確認 producer.py 可以與kafka 互動

```
docker pull apache/kafka:latest
docker run -d --name kafka -p 9092:9092 apache/kafka:latest
```



## 4. 再多部署一個 consumer 的資料讀取部分

## 5. demo 成品
