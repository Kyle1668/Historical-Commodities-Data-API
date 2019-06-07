FROM python:3.6.8-alpine

WORKDIR /usr/src/historical_commodities_data_api
COPY . /usr/src/historical_commodities_data_api

RUN pip3 install --user pipenv
ENV PATH="/root/.local/bin:${PATH}"
RUN pipenv install

ENV FLASK_ENV=production

EXPOSE 8080

CMD [ "pipenv", "run", "gunicorn", "-b", "0.0.0.0:8080", "wsgi" ]