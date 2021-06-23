SHELL = /bin/bash
USER := $(shell id -un)
PWD := $(shell pwd)

IMAGE_NAME = slapi
IMAGE_TAG = latest

DOCKER_BUILD = docker build -t $(IMAGE_NAME) .

ifeq ($(DOCKER_VOLUME),)
override DOCKER_VOLUME := "$(PWD):/slapi"
endif

ifeq ($(DOCKER_WORKDIR),)
override DOCKER_WORKDIR := "/slapi"
endif

DOCKER_RUN := docker run --rm=true --privileged \
    -v $(DOCKER_VOLUME) \
    -w $(DOCKER_WORKDIR) \
    -e "http_proxy=$(http_proxy)" \
    -e "https_proxy=$(https_proxy)" \
    -i$(if $(TERM),t,)


.PHONY: slapi-bash
.DEFAULT_GOAL := slapi-bash

build:
	$(DOCKER_BUILD) ;

tutorial: build
	$(DOCKER_RUN) -t $(IMAGE_NAME):$(IMAGE_TAG) \
	make -C grpc/go/src/tutorial

bindings: build
	$(DOCKER_RUN) -t $(IMAGE_NAME):$(IMAGE_TAG) \
	bash -c "cd grpc/utils && ./gen-all.sh"

xr-docs: build
	$(DOCKER_RUN) -t $(IMAGE_NAME):$(IMAGE_TAG) \
	bash -c "cd grpc/xrdocs/scripts && ./doc-gen.sh"

docs: build
	$(DOCKER_RUN) -t $(IMAGE_NAME):$(IMAGE_TAG) \
	bash -c "cd grpc/docs/scripts && ./doc-gen.sh"

slapi-bash: build
	$(DOCKER_RUN) -t $(IMAGE_NAME):$(IMAGE_TAG) bash
