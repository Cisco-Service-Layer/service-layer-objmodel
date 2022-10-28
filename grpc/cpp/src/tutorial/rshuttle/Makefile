TARGET := servicelayermain 
SRC_FILES := $(wildcard *.cpp)
OBJ_FILES := $(patsubst %.cpp,%.o,$(SRC_FILES))
# LDFLAGS from https://github.com/grpc/grpc/blob/master/examples/cpp/helloworld/Makefile#L23
LDFLAGS := -L${HOME}/.local/lib -L/usr/local/lib -liosxrsl `PKG_CONFIG_PATH=${HOME}/.local/lib/pkgconfig pkg-config --libs protobuf grpc++ libglog`  -lcares -lupb -laddress_sorting -lz \
	-pthread -Wl,--no-as-needed -lgrpc++_reflection -Wl,--as-needed -ldl
# CPPFLAGS set based on  https://github.com/grpc/grpc/blob/master/examples/cpp/helloworld/Makefile#L20
CPPFLAGS := -g -std=c++11 -pthread `PKG_CONFIG_PATH=${HOME}/.local/lib/pkgconfig pkg-config --cflags protobuf grpc++ libglog`

.PHONY: all
all: $(TARGET)

%.o: %.cc
	g++ $(CPPFLAGS) -c -o $@ $<

$(TARGET): $(OBJ_FILES)
	g++ $^ $(LDFLAGS) -o $@


.PHONY: clean
clean:
	-${RM} ${TARGET} ${OBJ_FILES}
