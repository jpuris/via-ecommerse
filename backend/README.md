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

### Manually

It is assumed you have MongoDB DB available, see the ENV variables below. Docker solution creates the db container.

#### Create virtual env and activate it

```sh
virtualenv venv
source venv/bin/activate
```

#### Install requirements

```sh
pip install -r requirements.txt
```

#### Run

```sh
# Local MongoDB instance reachable on localhost.
# Database name is "app"
export MONGODB_URL="mongodb://127.0.0.1:27017"
export MONGODB_DB_NAME="app"
python app/main.py
```

Access the docs at http://127.0.0.1:8000/docs

## Additional environmental variables

- *DEBUG_MODE* possible values are (TRUE, FALSE). Enable or disable FastAPI debug mode. Default is False
- *APP_NAME* application name. Default is "app"
- *APP_HOST* application host IP. Defaults to "127.0.0.1"
- *APP_PORT* application port. Defaults to "8000"

## License
MIT
