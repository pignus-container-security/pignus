# Install Mysql Through Helm
helm repo add bitnami https://charts.bitnami.com/bitnami
helm upgrade --install mysql --namespace=pignus-cicd bitnami/mysql