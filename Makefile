SHELL = /bin/bash
USER := $(shell id -un)
PWD := $(shell pwd)

IMAGE_NAME = slapi
IMAGE_TAG = $(shell cat Dockerfile | shasum | awk '{print substr($$1,0,11);}')

DOCKER_BUILD = docker build --no-cache \
               -t $(IMAGE_NAME) . && \
               docker tag $(IMAGE_NAME):latest $(IMAGE_NAME):$(IMAGE_TAG)

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

tutorial:
	@docker inspect --type image $(IMAGE_NAME):$(IMAGE_TAG) &> /dev/null || \
	{ echo Image $(IMAGE_NAME):$(IMAGE_TAG) not found. Building... ; \
	$(DOCKER_BUILD) ; }
	$(DOCKER_RUN) -t $(IMAGE_NAME):$(IMAGE_TAG) \
	make -C grpc/go/src/tutorial

bindings:
	@docker inspect --type image $(IMAGE_NAME):$(IMAGE_TAG) &> /dev/null || \
	{ echo Image $(IMAGE_NAME):$(IMAGE_TAG) not found. Building... ; \
	$(DOCKER_BUILD) ; }
	$(DOCKER_RUN) -t $(IMAGE_NAME):$(IMAGE_TAG) \
	bash -c "cd grpc/utils && ./gen-all.sh"

slapi-bash:
	@docker inspect --type image $(IMAGE_NAME):$(IMAGE_TAG) &> /dev/null || \
		{ echo Image $(IMAGE_NAME):$(IMAGE_TAG) not found. Building... ; \
		$(DOCKER_BUILD) ; }
	$(DOCKER_RUN) -t $(IMAGE_NAME):$(IMAGE_TAG) bash
