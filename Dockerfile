ARG UBUNTU_VER=20.04
FROM ubuntu:${UBUNTU_VER}
# Here we define UBUNTU_VER again, so it can be used after FROM.
ARG UBUNTU_VER

# https://askubuntu.com/questions/909277/avoiding-user-interaction-with-tzdata-when-installing-certbot-in-a-docker-contai/1098881#1098881
RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone

RUN apt-get update && \
    apt-get install -y git vim doxygen autoconf automake libtool \
                       build-essential pkg-config curl make \
                       unzip python3 python3-pip python3-venv wget libssl-dev

# python
RUN python3 -m venv /opt/venv
RUN . /opt/venv/bin/activate
COPY grpc/python/requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

ARG GO_VER=1.19
ARG WS=/ws
RUN mkdir -p ${WS}
WORKDIR ${WS}
ARG PROTOC_VER=3.18.3

# Install GO binary https://go.dev/doc/install
RUN wget -qO- https://golang.org/dl/go${GO_VER}.linux-amd64.tar.gz | tar xzvf - -C /usr/local

#Ensure PATH has GO binary path
ENV PATH="${PATH}:/usr/local/go/bin"

# Avoid timezone prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install .NET SDK
RUN wget -q  -O packages-microsoft-prod.deb https://packages.microsoft.com/config/ubuntu/${UBUNTU_VER}/packages-microsoft-prod.deb
RUN dpkg -i packages-microsoft-prod.deb
RUN apt-get update && apt-get install -y dotnet-sdk-6.0
RUN rm packages-microsoft-prod.deb

# Disable .NET CLI's telemetry feature
ENV DOTNET_CLI_TELEMETRY_OPTOUT=1

# Install protocol buffer compiler https://grpc.io/docs/protoc-installation/
ARG PB_REL=https://github.com/protocolbuffers/protobuf/releases
RUN curl -LO ${PB_REL}/download/v${PROTOC_VER}/protoc-${PROTOC_VER}-linux-x86_64.zip
RUN unzip protoc-${PROTOC_VER}-linux-x86_64.zip -d /usr/local

# Install protoc-gen-go and protoc-gen-go-grpc
# Reference https://grpc.io/docs/languages/go/quickstart

RUN go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.28
RUN go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.2

# Above were installed in $HOME/go, since this is running as root
ENV PATH="${PATH}:/root/go/bin"

####################

# CPP grpc build and install
# reference https://grpc.io/docs/languages/cpp/quickstart
ARG MY_INSTALL_DIR=/root/.local
RUN mkdir -p ${MY_INSTALL_DIR}

ENV PATH="${PATH}:${MY_INSTALL_DIR}/bin"

#get cmake
RUN wget -q -O cmake-linux.sh https://github.com/Kitware/CMake/releases/download/v3.21.7/cmake-3.21.7-Linux-x86_64.sh
RUN sh cmake-linux.sh -- --skip-license --prefix=${MY_INSTALL_DIR}

# Clone GRPC repo
RUN git clone --recurse-submodules -b v1.46.3 --depth 1 --shallow-submodules https://github.com/grpc/grpc
WORKDIR ${WS}/grpc

RUN mkdir -p cmake/build
WORKDIR ${WS}/grpc/cmake/build
RUN cmake -DgRPC_INSTALL=ON -DgRPC_BUILD_TESTS=OFF -DCMAKE_INSTALL_PREFIX=${MY_INSTALL_DIR} ../..
RUN make -j
RUN make install
WORKDIR ${WS}

############

# Clone glog repo. this is required for the CPP rshuttle application.
RUN git clone https://github.com/google/glog.git -b v0.6.0-rc2 glog
WORKDIR ${WS}/glog

# Configure build tree
# Installs glog in the install directory so it can be linked
RUN cmake -S . -B build -G "Unix Makefiles" -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX=${MY_INSTALL_DIR}
RUN cmake --build build
RUN cmake --build build --target install

###########
# Adjust PATH so that binding scripts can execute out of the cwd.
ENV PATH="${PATH}:."
