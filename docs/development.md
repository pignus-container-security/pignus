# Pignus Development
To develop on Pignus, download the repository and set an environment variable, `PIGNUS_PATH` to the
location where Pignus is installed. Details on developing each piece of Pignus are described below.

## Components
### Pignus-Api
Located at `pignus/src/pignus-api`. This Python project runs the web REST API for Pignus.

### Pignus-Sentry
Located at `pignus/src/pignus-sentry`.

## Testing
### Unit Tests
Unit tests are managed by Oytest, and can be found in [tests/unit](../tests/unit).
To execute unit tests go to the unit test dir and run `pytest -vvv`.
To get test coverage `pytest -vv --cov=pignus --cov-report term-missing`
Current unit test coverage at _49%_ with 261 unit tests.
### Regression Tests
Regression tests are managed by pytest, and can be found in [tests/regression](../tests/regression).
They cover each of the entities the API currently exposes.



## House Keeping
When pressing a new sem ver the following files will need to be updated.
`README.md`
`/pignus/src/pignus/version.py`


# Helper Commands
Random smattering of helper commands used in developing/ working with Pignus.

kubectl create job -n secops --from=cronjob/pignus-theia pignus-theia-manual-001

helm upgrade \
  --install \
  pignus-theia \
  ./helm/theia  \
  -n secops \
  -f ./helm/theia/values.yaml \
  -f ./helm/theia/stage-values.yaml
```
