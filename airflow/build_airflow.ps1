$tag = ([System.Guid]::NewGuid()).ToString().Substring(0,8)
docker build --pull --tag "fwwhahn/whahn-airflow:$tag" .
docker push "fwwhahn/whahn-airflow:$tag";

helm upgrade --install airflow apache-airflow/airflow --create-namespace --namespace bdo-provider `
  --set images.airflow.repository=fwwhahn/whahn-airflow `
  --set images.airflow.tag=$tag;
kubectl scale -n bdo-provider statefulset airflow-worker --replicas=5;
Start-Sleep -Seconds 60;
kubectl port-forward svc/airflow-webserver 8080:8080 --namespace bdo-provider &
