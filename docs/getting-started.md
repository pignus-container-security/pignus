# Getting Started
Pignus is currently built to run on AWS. Pignus utilizes AWS Lambda, CodeBuild, ECR and RDS to
perform. Full installation docs can be found at [Pignus Getting Started](docs/getting-started.md).


## Install Pignus-Api

```console
helm install 

helm upgrade \
  --install \
  pignus-api-dev \
  ./helm/pignus-api \
  -n pignus-dev \
  -f ./helm/pignus-api/values.yaml \
  -f ./helm/pignus-api/dev-values.yaml
