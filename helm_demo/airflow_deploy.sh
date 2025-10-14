helm repo add bitnami https://charts.bitnami.com/bitnami
helm search repo airflow
helm pull --untar bitnami/airflow
helm install airflow-1 ./airflow
