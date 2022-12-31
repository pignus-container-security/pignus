# Pignus-Api
# This container runs the Pignus web api
#

FROM politeauthority/pignus-api:latest

ENV PIGNUS_API_URL=""
ENV PIGNUS_API_CLIENT_ID=""

ADD regression /tests

RUN apk add bash vim
RUN pip3 install -r /tests/requirements.txt

CMD cd /tests && pytest
