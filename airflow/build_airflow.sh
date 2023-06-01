tag=$(uuidgen | cut -d'-' -f1)
docker build --pull --tag "fwwhahn/whahn-airflow:$tag"
docker push "fwwhahn/whahn-airflow:$tag"
