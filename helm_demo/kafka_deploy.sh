helm uninstall kafka-1
helm repo add kafka-repo https://helm-charts.itboon.top/kafka
helm repo update kafka-repo
helm pull --untar kafka-repo/kafka
helm install kafka-1 ./kafka