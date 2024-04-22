SHELL = /bin/bash
USER := $(shell id -un)
PWD := $(shell pwd)

IMAGE_NAME = slapi
IMAGE_TAG = latest
CONTAINER_NAME = slapi-container

DOCKER_BUILD = docker build -t $(IMAGE_NAME) .

ifeq ($(DOCKER_VOLUME),)
override DOCKER_VOLUME := "$(PWD):/slapi"
endif

ifeq ($(DOCKER_WORKDIR),)
override DOCKER_WORKDIR := "/slapi"
endif

DOCKER_RUN := docker run --name $(CONTAINER_NAME) --rm=true --privileged \
    -v $(DOCKER_VOLUME) \
    -w $(DOCKER_WORKDIR) \
    -e "http_proxy=$(http_proxy)" \
    -e "https_proxy=$(https_proxy)" \
    -i$(if $(TERM),t,)

# New clean target to remove the container and image
clean:
	-docker rm -f $(CONTAINER_NAME)
	-docker rmi -f $(IMAGE_NAME):$(IMAGE_TAG)

.PHONY: slapi-bash
.DEFAULT_GOAL := slapi-bash

build:
	$(DOCKER_BUILD) ;

tutorial: build bindings
	$(DOCKER_RUN) -t $(IMAGE_NAME):$(IMAGE_TAG) \
	make -C grpc/go/src/tutorial

cpp-tutorial: build bindings
	$(DOCKER_RUN) -t $(IMAGE_NAME):$(IMAGE_TAG) \
	bash -c "make -C grpc/cpp/src all && \
			make -C grpc/cpp/src install && \
			make -C grpc/cpp/src/tutorial && \
			make -C grpc/cpp/src/tutorial/rshuttle"

bindings: build
	$(DOCKER_RUN) -t $(IMAGE_NAME):$(IMAGE_TAG) \
	bash -c "cd grpc/utils && ./gen-all.sh"

xr-docs: build
	$(DOCKER_RUN) -t $(IMAGE_NAME):$(IMAGE_TAG) \
	bash -c "cd grpc/xrdocs/scripts && ./doc-gen.sh"

dotnet-docs: build
	$(DOCKER_RUN) -t $(IMAGE_NAME):$(IMAGE_TAG) \
	bash -c "cd grpc/dotnet/ && doxygen ./doxyfile"

slapi-bash: build
	$(DOCKER_RUN) -t $(IMAGE_NAME):$(IMAGE_TAG) bash

