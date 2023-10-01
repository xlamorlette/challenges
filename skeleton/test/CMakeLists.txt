add_executable(skeleton_test
    A_test.cpp
)

target_link_libraries(skeleton_test
    PRIVATE
        Catch2::Catch2WithMain
        skeleton_lib
)

include(CTest)
include(Catch)

catch_discover_tests(skeleton_test)
