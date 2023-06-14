minikube start;
minikube dashboard &;
kubectl port-forward svc/airflow-webserver 8080:8080 --namespace bdo-provider &;
kubectl port-forward -n bdo-provider svc/postgres-data-postgresql 5433:5432 &;
