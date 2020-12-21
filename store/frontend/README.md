# via-ecommerse-store

# WEB

Simple item store UI service written with VueJS and VueJS Bootstrap.
Requires running backend. See [store backend](../backend/README.md)

## Stack
- Node
- VueJS + VueJS Bootstrap

## How to run it

Clone the repository
```
git clone git@github.com:jpuris/via-ecommerse-store
cd via-ecommerse-store/frontend
```

### Docker

Requires
- Docker
- Docker compose

```sh
docker-compose up --build 
```

Access the UI at http://localhost:8180

#### Cleanup

```shell
docker-compose rm
```

## Project setup

You must have npm and node installed on your system.

### Manually
```
npm install -g @vue/cli@3.7.0
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

