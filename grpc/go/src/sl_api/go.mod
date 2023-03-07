module sl_api

go 1.19

require (
	gengo v0.0.0-00010101000000-000000000000
	github.com/sirupsen/logrus v1.9.0
	golang.org/x/net v0.7.0
	google.golang.org/grpc v1.49.0
)

require (
	github.com/golang/protobuf v1.5.2 // indirect
	golang.org/x/sys v0.5.0 // indirect
	golang.org/x/text v0.7.0 // indirect
	google.golang.org/genproto v0.0.0-20200526211855-cb27e3aa2013 // indirect
	google.golang.org/protobuf v1.27.1 // indirect
)

replace gengo => ../gengo
