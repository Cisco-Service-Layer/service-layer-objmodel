TARGET := quickstart
SRC_FILES := quickstart.cc
OBJ_FILES := quickstart.o 
# LDFLAGS from https://github.com/grpc/grpc/blob/master/examples/cpp/helloworld/Makefile#L23
# pkg-config does not pickup cares and ubp for some reason, so explicitly enumerated.
LDFLAGS := -L${HOME}/.local/lib -L/usr/local/lib -liosxrsl `PKG_CONFIG_PATH=${HOME}/.local/lib/pkgconfig pkg-config --libs protobuf grpc++_unsecure`  -lcares -lupb -laddress_sorting -lz \
	-pthread -Wl,--no-as-needed -lgrpc++_reflection -Wl,--as-needed -ldl

# CPPFLAGS set based on  https://github.com/grpc/grpc/blob/master/examples/cpp/helloworld/Makefile#L20
CPPFLAGS := -g -std=c++11 -pthread `PKG_CONFIG_PATH=${HOME}/.local/lib/pkgconfig pkg-config --cflags protobuf grpc++_unsecure`

.PHONY: all
all: $(TARGET)

%.o: %.cc
	g++ $(CPPFLAGS) -c -o $@ $<

$(TARGET): $(OBJ_FILES)
	g++ $^ $(LDFLAGS) -o $@


.PHONY: clean
clean:
	-${RM} ${TARGET} ${OBJ_FILES}
