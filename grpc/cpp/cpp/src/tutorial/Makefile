TARGET := quickstart
SRC_FILES := quickstart.cc
OBJ_FILES := quickstart.o 
LDFLAGS := -L/usr/local/lib  -I/usr/local/include -lgrpc++_unsecure -lgrpc -lprotobuf -lpthread -ldl -liosxrsl
CPPFLAGS := -g -std=c++11 -I/usr/local/include -pthread

.PHONY: all
all: $(TARGET)

%.o: %.cc
	g++ $(CPPFLAGS) -c -o $@ $<

$(TARGET): $(OBJ_FILES)
	g++ $^ $(LDFLAGS) -o $@


.PHONY: clean
clean:
	-${RM} ${TARGET} ${OBJ_FILES}
