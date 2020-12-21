# via-ecommerse-store

# API

Simple item store API service written in Python.
It stores items in external MongoDB database and has various endpoints to retrieve and manipulate the data stored in it.

## Stack
- FastAPI
- MongoDB

# WEB

Simple item store UI service written with VueJS and VueJS Bootstrap.

## Stack
- Node
- VueJS + VueJS Bootstrap

## How to run it

Clone the repository
```
git clone git@github.com:jpuris/via-ecommerse
cd via-ecommerse/store
```

### Docker

#### Requires
- docker
- docker-compose

```sh
docker-compose up --build 
```

- Access the OpenAPI UI at http://localhost:8100/docs
- Access the WEB UI at http://localhost:8080

#### Cleanup

```shell
docker-compose up rm
```