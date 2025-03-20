
GO_BIN_NAME = tutorial_slaf

.PHONY: go-pkgs
.DEFAULT_GOAL := go-bin

gen-bindings:
	cd /slapi/grpc/go && ./gen-bindings.sh

go-bin: gen-bindings
	go build -o $(GO_BIN_NAME) -buildvcs=false

clean:
	rm -f $(GO_BIN_NAME)
