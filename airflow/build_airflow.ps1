$tag = ([System.Guid]::NewGuid()).ToString().Substring(0,8)
docker build --pull --tag "fwwhahn/whahn-airflow:$tag" .
docker push "fwwhahn/whahn-airflow:$tag";

helm upgrade --install airflow apache-airflow/airflow --create-namespace --namespace bdo-airflow `
  --set images.airflow.repository=fwwhahn/whahn-airflow `
  --set images.airflow.tag=$tag
