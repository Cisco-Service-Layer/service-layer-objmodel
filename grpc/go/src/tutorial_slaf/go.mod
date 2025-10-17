module tutorial_slaf

go 1.24.3

require (
	gengo v0.0.0-00010101000000-000000000000
	github.com/sirupsen/logrus v1.9.0
	google.golang.org/grpc v1.72.2
	sl_api_slaf v0.0.0-00010101000000-000000000000
	util v0.0.0-00010101000000-000000000000
)

require (
	golang.org/x/net v0.44.0 // indirect
	golang.org/x/sys v0.36.0 // indirect
	golang.org/x/text v0.29.0 // indirect
	google.golang.org/genproto v0.0.0-20230410155749-daa745c078e1 // indirect
	google.golang.org/protobuf v1.36.6 // indirect
)

replace gengo => ../gengo

replace sl_api_slaf => ../sl_api_slaf

replace util => ../util
