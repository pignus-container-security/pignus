# Pignus v0.0.1

Pignus was an internal tool developed by [Alix Fullerton](https://github.com/politeauthority).


Pignus aims to provide the SecOps teams details on workloads deployed to Kubernetes clusters. It
provides vulnerability data on images deployed to clusters in real time and historically.

# How it Works
Pignus is comprised of multiple pieces.
 - **Pignus CLI** - A client CLI tool that queries the Pignus Api providing details on Kubernetes workloads.
 - **Theia** - A Helm chart deployed to Kubernetes clusters which scrapes the Kubernetes Api for details on container images running in a cluster.
 - **Pignus Api** - A REST api which provides access to the Pignus database
 - **Sentry** - A cron process which makes sure that container scans are run regularly.

# Getting Started
Pignus is currently built to run on AWS. Pignus utilizes AWS Lambda, CodeBuild, ECR and RDS to
perform. Full installation docs can be found at [Pignus Getting Started](docs/getting-started.md).

# Development
Details on how Pignus is built, tested and deployed can be found at
[Pignus Development](docs/development.md). Note: This document does not include contributor
guidelines yet, this doc solely describes how to build and test Pignus as well as information around
the project's development.


