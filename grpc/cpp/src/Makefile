CPPFLAGS := -g -std=c++11 -I/root/.local/include -pthread
RM = rm -f  # rm command
TARGET_LIB = libiosxrsl.a # target lib
LIBDIR = /usr/local/lib/
INCLUDEDIR = /usr/local/include/iosxrsl

SRC_FILES := $(wildcard gencpp/*.cc)
OBJ_FILES := $(patsubst gencpp/%.cc,genobj/%.o,$(SRC_FILES))
INC_FILES := $(wildcard gencpp/*.h)

.PHONY: all
all: $(TARGET_LIB)

genobj/%.o: gencpp/%.cc
	mkdir -p genobj
	g++ $(CPPFLAGS) -c -o $@ $<


$(TARGET_LIB): $(OBJ_FILES)
	ar rcv $(TARGET_LIB) $^
	ranlib $(TARGET_LIB)
	
.PHONY: install
install:
	mkdir -p $(LIBDIR)
	mkdir -p $(INCLUDEDIR)
	cp -p $(TARGET_LIB) $(LIBDIR)
	cp -p $(INC_FILES) $(INCLUDEDIR)

.PHONY: clean
clean:
	-${RM} ${TARGET_LIB} ${OBJ_FILES} ${SRC_FILES} ${INC_FILES}
