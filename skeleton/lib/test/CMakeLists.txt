set(SOURCE_FILES
    A_test.cpp
)

add_executable(skeleton_test ${SOURCE_FILES})

target_include_directories(skeleton_test PRIVATE ..)

target_compile_options(skeleton_test PRIVATE ${COMPILE_OPTIONS})

target_link_libraries(skeleton_test
    PRIVATE
        Catch2::Catch2WithMain
        skeleton_lib
)

include(CTest)
include(Catch)

catch_discover_tests(skeleton_test)
