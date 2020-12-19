NAME = via-ecommerse-warehouse-backend-api
TAG = $$(git log -1 --pretty=%h)
IMG = ${NAME}-${TAG}
LATEST = ${NAME}:latest

build:
	docker build -t ${IMG} .
	docker tag ${IMG} ${LATEST}

run:
	docker-compose -f docker-compose.yaml up

default: build
