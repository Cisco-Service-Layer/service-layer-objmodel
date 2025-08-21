module sl_api

go 1.24.3

require (
	gengo v0.0.0-00010101000000-000000000000
	github.com/sirupsen/logrus v1.9.0
	golang.org/x/net v0.36.0
	google.golang.org/grpc v1.72.2
)

require (
	golang.org/x/sys v0.30.0 // indirect
	golang.org/x/text v0.22.0 // indirect
	google.golang.org/genproto v0.0.0-20230410155749-daa745c078e1 // indirect
	google.golang.org/protobuf v1.36.6 // indirect
)

replace gengo => ../gengo
