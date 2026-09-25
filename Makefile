CXX ?= g++
CXXFLAGS = -std=c++17 -O2 -Wall -Wextra

all: build/test_suffix_array build/sa_trace

build/test_suffix_array: src/test_suffix_array.cpp src/suffix_array.hpp
	@mkdir -p build
	$(CXX) $(CXXFLAGS) $< -o $@

build/sa_trace: src/trace_main.cpp src/suffix_array.hpp
	@mkdir -p build
	$(CXX) $(CXXFLAGS) $< -o $@

test: build/test_suffix_array
	./build/test_suffix_array

clean:
	rm -rf build
