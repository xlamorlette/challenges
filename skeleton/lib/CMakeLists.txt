set(SOURCE_FILES
    A.cpp
    A.hpp
)

add_library(skeleton_lib STATIC ${SOURCE_FILES})

target_compile_options(skeleton_lib PRIVATE ${COMPILE_OPTIONS})

add_subdirectory(test)
