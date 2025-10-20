helm search hub kafka
helm search repo kafka
helm pull --untar bitnami/kafka
helm install kafka-1 ./kafka
helm uninstall kafka-1