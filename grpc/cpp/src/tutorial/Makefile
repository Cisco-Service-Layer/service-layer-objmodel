TARGET := quickstart
SRC_FILES := quickstart.cc
OBJ_FILES := quickstart.o 
LDFLAGS := -L/root/.local/lib -L/usr/local/lib  -I/root/.local/include -lprotobuf -lgrpc++ -lpthread -ldl -liosxrsl -L/root/.local/lib -lprotobuf -pthread -lgrpc++_unsecure -lgrpc_unsecure -lgpr -labsl_raw_hash_set -labsl_hashtablez_sampler -labsl_hash -labsl_city -labsl_low_level_hash -labsl_random_distributions -labsl_random_seed_sequences -labsl_random_internal_pool_urbg -labsl_random_internal_randen -labsl_random_internal_randen_hwaes -labsl_random_internal_randen_hwaes_impl -labsl_random_internal_randen_slow -labsl_random_internal_platform -labsl_random_internal_seed_material -labsl_random_seed_gen_exception -labsl_statusor -labsl_status -labsl_cord -labsl_cordz_info -labsl_cord_internal -labsl_cordz_functions -labsl_exponential_biased -labsl_cordz_handle -labsl_bad_optional_access -labsl_str_format_internal -labsl_synchronization -labsl_graphcycles_internal -labsl_stacktrace -labsl_symbolize -labsl_debugging_internal -labsl_demangle_internal -labsl_malloc_internal -labsl_time -labsl_civil_time -labsl_strings -labsl_strings_internal -lrt -labsl_base -labsl_spinlock_wait -labsl_int128 -labsl_throw_delegate -labsl_time_zone -labsl_bad_variant_access -labsl_raw_logging_internal -labsl_log_severity -lcares -lupb -laddress_sorting -lz -lgrpc++_reflection

CPPFLAGS := -g -std=c++11 -I/root/.local/include -pthread -DNOMINMAX -maes -msse4.1 -DNOMINMAX -maes -msse4.1 -DNOMINMAX -I/root/.local/include

.PHONY: all
all: $(TARGET)

%.o: %.cc
	g++ $(CPPFLAGS) -c -o $@ $<

$(TARGET): $(OBJ_FILES)
	g++ $^ $(LDFLAGS) -o $@


.PHONY: clean
clean:
	-${RM} ${TARGET} ${OBJ_FILES}
