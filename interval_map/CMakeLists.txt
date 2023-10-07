cmake_minimum_required(VERSION 3.26)

project(interval_map)

include(../CMakeListsCommon.cmake)

set(SOURCE_FILES
    interval_map_test.cpp
    interval_map.hpp
)

add_executable(interval_map_lib_test ${SOURCE_FILES})

target_include_directories(interval_map_lib_test PRIVATE ..)

target_compile_options(interval_map_lib_test PRIVATE ${COMPILE_OPTIONS})

target_link_libraries(interval_map_lib_test
    PRIVATE
        Catch2::Catch2WithMain
)

include(CTest)
include(Catch)

catch_discover_tests(interval_map_lib_test)
