FROM python:3.6.8-alpine3.9

ENV PATH="/root/.local/bin:${PATH}" \
    PYTHONPATH=/usr/src/historical_commodities_data_api

WORKDIR /usr/src/historical_commodities_data_api
COPY . /usr/src/historical_commodities_data_api

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev

RUN pip3 install --upgrade pip
RUN pip3 install --user flask \
                        requests \
                        beautifulsoup4 \
                        numpy \
                        gunicorn \
                        psycopg2 \
                        flask-restful \
                        jinja2 \
                        python-dateutil \
                        python-dotenv

EXPOSE 8080

CMD [ "python", "api.py" ]