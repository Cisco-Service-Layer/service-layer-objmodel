module tutorial

go 1.19

require (
	gengo v0.0.0-00010101000000-000000000000
	github.com/sirupsen/logrus v1.9.0
	google.golang.org/grpc v1.53.0
	sl_api v0.0.0-00010101000000-000000000000
	util v0.0.0-00010101000000-000000000000
)

require (
	github.com/golang/protobuf v1.5.2 // indirect
	golang.org/x/net v0.7.0 // indirect
	golang.org/x/sys v0.5.0 // indirect
	golang.org/x/text v0.7.0 // indirect
	google.golang.org/genproto v0.0.0-20230110181048-76db0878b65f // indirect
	google.golang.org/protobuf v1.28.1 // indirect
)

replace gengo => ../gengo

replace sl_api => ../sl_api

replace util => ../util
