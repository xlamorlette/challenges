cmake_minimum_required(VERSION 3.26)

include(../CMakeListsCommon.cmake)

project(main)

set(SOURCE_FILES
    main.cpp
)

add_executable(main ${SOURCE_FILES})

target_compile_options(main PRIVATE ${COMPILE_OPTIONS})
