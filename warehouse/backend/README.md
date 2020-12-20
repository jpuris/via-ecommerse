# via-ecommerse-warehouse

# API

Simple item warehouse API service written in Python.
It stores items in external MongoDB database and has various endpoints to retrieve and manipulate the data stored in it.

## Stack
- FastAPI
- MongoDB

## How to run it

Clone the repository
```shell
git clone git@github.com:jpuris/via-ecommerse-warehouse
cd via-ecommerse-warehouse/backend
```

### Docker

Requires
- Docker
- Docker compose

```shell
docker-compose up --build 
```

Access the OpenAPI UI at http://localhost:8000/docs

#### Cleanup

```shell
docker compose rm
```

## License
MIT
