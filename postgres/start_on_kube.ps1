helm repo add bitnami https://charts.bitnami.com/bitnami; helm repo update;
kubectl apply -f pg_pv.yaml --namespace bdo-airflow;
kubectl apply -f pg_pv_claim.yaml --namespace bdo-airflow;
helm upgrade --install postgres-data -f secrets.yaml bitnami/postgresql --namespace bdo-airflow
