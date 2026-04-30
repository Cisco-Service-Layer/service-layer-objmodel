SHELL := /bin/bash

PWD := $(shell pwd)

IMAGE_NAME ?= slapi
IMAGE_TAG ?= latest
CONTAINER_NAME ?= slapi-container

DOCKER_VOLUME ?= $(PWD):/slapi
DOCKER_WORKDIR ?= /slapi

DOCKER_BUILD := docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

DOCKER_ENV := \
	-e "http_proxy=$(http_proxy)" \
	-e "https_proxy=$(https_proxy)" \
	-e "HTTP_PROXY=$(HTTP_PROXY)" \
	-e "HTTPS_PROXY=$(HTTPS_PROXY)" \
	-e "no_proxy=$(no_proxy)" \
	-e "NO_PROXY=$(NO_PROXY)"

DOCKER_RUN := docker run --name $(CONTAINER_NAME) --rm \
	-v "$(DOCKER_VOLUME)" \
	-w "$(DOCKER_WORKDIR)" \
	$(DOCKER_ENV)

DOCKER_RUN_TTY := docker run --name $(CONTAINER_NAME) --rm \
	-v "$(DOCKER_VOLUME)" \
	-w "$(DOCKER_WORKDIR)" \
	$(DOCKER_ENV) \
	-it

.PHONY: clean build bindings tutorial cpp-tutorial xr-docs dotnet-docs slapi-bash
.DEFAULT_GOAL := slapi-bash

clean:
	-docker rm -f $(CONTAINER_NAME)
	-docker rmi -f $(IMAGE_NAME):$(IMAGE_TAG)

build:
	$(DOCKER_BUILD)

bindings: build
	$(DOCKER_RUN) $(IMAGE_NAME):$(IMAGE_TAG) \
		bash -c "cd grpc/utils && ./gen-all.sh"

tutorial: build bindings
	$(DOCKER_RUN) $(IMAGE_NAME):$(IMAGE_TAG) \
		make -C grpc/go/src/tutorial

cpp-tutorial: build bindings
	$(DOCKER_RUN) $(IMAGE_NAME):$(IMAGE_TAG) \
		bash -c "make -C grpc/cpp/src all && \
		         make -C grpc/cpp/src install && \
		         make -C grpc/cpp/src/tutorial && \
		         make -C grpc/cpp/src/tutorial/rshuttle"

xr-docs: build
	$(DOCKER_RUN) $(IMAGE_NAME):$(IMAGE_TAG) \
		bash -c "cd grpc/xrdocs/scripts && ./doc-gen.sh"

dotnet-docs: build
	$(DOCKER_RUN) $(IMAGE_NAME):$(IMAGE_TAG) \
		bash -c "cd grpc/dotnet && doxygen ./doxyfile"

slapi-bash: build
	$(DOCKER_RUN_TTY) $(IMAGE_NAME):$(IMAGE_TAG) bash
