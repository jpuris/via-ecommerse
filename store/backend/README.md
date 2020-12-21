# via-ecommerse-store

# API

Simple item store API service written in Python.
It stores items in external MongoDB database and has various endpoints to retrieve and manipulate the data stored
in it as well as to do full item sync with store via store API.

## Stack
- FastAPI
- MongoDB

## How to run it

Clone the repository
```shell
git clone git@github.com:jpuris/via-ecommerse
cd via-ecommerse/store/backend
```

### Docker

#### Requires
- Docker
- Docker compose

```shell
docker-compose up --build 
```

Access the OpenAPI UI at http://localhost:8100/docs

#### Cleanup

```shell
docker-compose rm
```

### Manually

It is assumed you have MongoDB DB available, see the ENV variables below. Docker solution creates the db container.
If you require mongodb, fastest way is to run it on docker like so
```sh
docker run -d -p 127.0.0.1:27017:27017 --name mongodb mongo
```

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
# Database name is "store"
export MONGODB_URL="mongodb://127.0.0.1:27017"
export MONGODB_DB_NAME="store"
python app/main.py
```

Access the docs at http://localhost:8000/docs

## Additional environmental variables

- *DEBUG_MODE* possible values are (TRUE, FALSE). Enable or disable FastAPI debug mode. Default is False
- *APP_NAME* application name. Default is "store"
- *APP_HOST* application host IP. Defaults to "127.0.0.1"
- *APP_PORT* application port. Defaults to "8000"

## License
MIT
