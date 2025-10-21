# 如何達到 Producer 的測試？


## 1. 學會一個 python 執行檔的打包與部屬 

1. 建立 print hello word  python script 

see `test.py`

2. 安裝 綁定 k3d 的 image registry 

```
k3d cluster create mycluster --registry-create mycluster-registry:6002
docker ps -f name=mycluster-registry
```

3. 將 k3d 連結到 local registry: 

```
docker network connect k3d-k3s-default registry
```

4. 將 python script 與 requirements.txt 的安裝包進 image 中，放上 image registry 

```
docker login localhost:6002
>> username: jeffrey82221
>> password: xxx 
docker build -t test_hello:v0.0.3 .
docker tag test_hello:v0.0.3 localhost:6002/jeffrey82221/test_hello:v0.0.3
docker push localhost:6002/jeffrey82221/test_hello:v0.0.3
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

## 4. 再多部署一個 consumer 的資料讀取部分

## 5. demo 成品
