FROM python:3.6.8-alpine3.9

ENV FLASK_ENV=production \
    PATH="/root/.local/bin:${PATH}" \
    PYTHONPATH=/usr/src/historical_commodities_data_api

WORKDIR /usr/src/historical_commodities_data_api
COPY . /usr/src/historical_commodities_data_api
COPY ../Pipfile /usr/src/historical_commodities_data_api

RUN pip3 install --upgrade pip
RUN pip3 install --user pipenv
RUN pipenv install

EXPOSE 8080

CMD [ "pipenv", "run", "gunicorn", "-b", "0.0.0.0:8080", "wsgi" ]