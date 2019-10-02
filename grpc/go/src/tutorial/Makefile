
GO_BIN_NAME = tutorial

.PHONY: go-pkgs
.DEFAULT_GOAL := go-bin

GO_PKGS = github.com/sirupsen/logrus \
	  golang.org/x/net/context

go-pkgs:
	go get $(GO_PKGS)

gen-bindings:
	cd /slapi/grpc/go && ./gen-bindings.sh

go-bin: go-pkgs gen-bindings
	go build -o $(GO_BIN_NAME)

clean:
	rm -f $(GO_BIN_NAME)
