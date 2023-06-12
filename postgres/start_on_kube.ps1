helm repo add bitnami https://charts.bitnami.com/bitnami; helm repo update;
kubectl apply -f pg_pvc_pv.yaml --namespace bdo-provider;
helm upgrade --install postgres-data --set volumePermissions.enabled=true -f secrets.yaml bitnami/postgresql --namespace bdo-provider
