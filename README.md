# Historical Commodity (Gold/Silver) Price Data API

## Summary

This project pulls data from online gold and silver data, stores it in a relational database, and serves it via a REST API.

## Components

Web Scraper

- Selenium based Docker container that runs a Python script which pulls data from these two sources.
- Postgress Database with tables **Gold** and **Silver**.
- Flask REST API that reads from Postgres

## Technologies

- Python 3.6
- Flask
- Docker
- Selenium
- PostgreSQL

## How To Run

This system used Docker to build and run it's individual components. You will need to have Docker installed on your machine to build this project.

## Steps

Run the following steps in the project root directory.

1. Build the Docker images. `docker-compose build`

2. Start the Postgres database `docker-compose up -d database`

3. Start the web scraper to pull the commodity data. `docker-compose up web_scraper`

4. Start the REST API `docker-compose up api_server`

## Example Requests

### Pull gold data between June 1st and 10th 2019

```json
$ curl "http://127.0.0.1:8080/commodity?commodity_type=gold&start_date=2019-06-1&end_date=2019-06-10"

{
    "data":[{
        "2019-06-10":1324.7},
        {"2019-06-07":1341.2},
        {"2019-06-06":1337.6},
        {"2019-06-05":1328.3},
        {"2019-06-04":1323.4},
        {"2019-06-03":1322.7}],
    "mean":1329.65,
    "variance":51.71583333333292
}
```

### Bad Request: Don't include one of the dates

```json
$ curl "http://127.0.0.1:8080/commodity?commodity_type=gold&end_date=2019-06-10"

{
    "error": true,
    "message": "Incorrect or missing query parameters"
}
```

### Bad Request: Searching for a commodity that's not supported

```json
$ curl "http://127.0.0.1:8080/commodity?commodity_type=oil&start_date=2019-06-1&end_date=2019-06-10"

{
    "error": true,
    "message": "Incorrect commodity type (not gold or silver)"
}
```

## Next Steps

If I had more time or if this project was destined for production, I'd implement the following steps.

1. Write unit and integration tests.
2. Write more thorough API documentation.
3. Right now, you have to start each service in a particular order. This is to avoid a race condition where the scraper sends data to Postgres before it's ready. I'd write a handler to wait for when PSQL is prepared and then attempt to connect.
4. Add Python docstrings to all functions.
5. Serve the API server behind NGINX.
6. Better HTTP responses,
