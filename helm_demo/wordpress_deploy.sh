helm search hub wordpress
helm repo add bitnami https://charts.bitnami.com/bitnami
helm search repo wordpress
helm install release-1 bitnami/wordpress
helm pull --untar bitnami/wordpress
helm uninstall release-1
helm install release-1 ./wordpress
helm uninstall release-1