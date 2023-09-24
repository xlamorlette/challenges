cmake_minimum_required(VERSION 3.26)

include(../CMakeListsCommon.cmake)

project(main)

set(SOURCE_FILES
    A.cpp
    A.hpp
    main.cpp
)

find_package(ZLIB REQUIRED)

add_executable(${PROJECT_NAME} ${SOURCE_FILES})

target_compile_options(${PROJECT_NAME} PRIVATE ${COMPILE_OPTIONS})

target_link_libraries(${PROJECT_NAME} ZLIB::ZLIB)
