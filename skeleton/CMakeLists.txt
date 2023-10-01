cmake_minimum_required(VERSION 3.26)

include(../CMakeListsCommon.cmake)

include_directories(${CMAKE_CURRENT_LIST_DIR})

project(skeleton)

set(SOURCE_FILES
    A.cpp
    A.hpp
)

add_library(skeleton_lib STATIC ${SOURCE_FILES})

target_compile_options(skeleton_lib PRIVATE ${COMPILE_OPTIONS})

add_subdirectory(command_line)
add_subdirectory(test)
