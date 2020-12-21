# via-ecommerse-warehouse

# API

Simple item warehouse API service written in Python.
It stores items in external MongoDB database and has various endpoints to retrieve and manipulate the data stored in it.

## Stack
- FastAPI
- MongoDB

# WEB

Simple item warehouse UI service written with VueJS and VueJS Bootstrap.

## Stack
- Node
- VueJS + VueJS Bootstrap

## How to run it

Clone the repository
```
git clone git@github.com:jpuris/via-ecommerse
cd via-ecommerse/warehouse
```

### Docker

Requires
- Docker

```sh
docker-compose up --build 
```

- Access the OpenAPI UI at http://localhost:8000/docs
- Access the WEB UI at http://localhost:8180

#### Cleanup

```shell
docker-compose rm
```