FROM python:alpine3.9
COPY . /app
WORKDIR /app
run pip3 install --upgrade pip
run pip install newrelic
RUN pip install -r requirements.txt
EXPOSE 5000
CMD NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program python3 create_order_api.py
