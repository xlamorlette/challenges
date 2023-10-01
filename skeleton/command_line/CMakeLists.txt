set(SOURCE_FILES
    main.cpp
)

find_package(ZLIB REQUIRED)

add_executable(command_line ${SOURCE_FILES})

target_include_directories(command_line PRIVATE ../lib)

target_compile_options(command_line PRIVATE ${COMPILE_OPTIONS})

target_link_libraries(command_line
    PRIVATE
        ZLIB::ZLIB
        skeleton_lib
)
