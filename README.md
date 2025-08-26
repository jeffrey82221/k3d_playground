# k3d_playground

Study using Helm Chart to Deploy Services onto K8S (simulated by K3D)

# Installation 

`brew install k3d`

# Start K3D cluster 

1. Create a cluster with 3 nodes 

`k3d cluster create -s 3`

2. Check cluster nodes

`k3d node list`

>> 
```
NAME                       ROLE           CLUSTER       STATUS
k3d-k3s-default-server-0   server         k3s-default   running
k3d-k3s-default-server-1   server         k3s-default   running
k3d-k3s-default-server-2   server         k3s-default   running
k3d-k3s-default-serverlb   loadbalancer   k3s-default   running
k3d-k3s-default-tools                     k3s-default   running
```


3. Switch to context 

`kubectl config use-context k3d-k3s-default`

4. Check node status using kubectl

`kubectl get nodes`

5. Check cluster-info

`kubectl cluster-info`
>> 

6. close k3d cluster and remove all nodes

```
k3d cluster stop
k3d cluster delete --all
```

7. start new pod with a image

```
kubectl run nginx --image=nginx
```

# Run a docker image on k3d nodes

# Debug inside a k3d node 



## check images of node `f7b8653d1695`

`docker exec -it f7b8653d1695 crictl images`

## check pods of node `f7b8653d1695`

`docker exec -it f7b8653d1695 crictl pods`

## check containers of node `f7b8653d1695`

`docker exec -it f7b8653d1695 crictl ps -a`

# Reference: 

https://barry-cheng.medium.com/雲端工程師在k3d上的初體驗-c2d92a37c09f