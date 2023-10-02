#include <A.hpp>

#include <catch2/catch_all.hpp>

TEST_CASE("A constructor") {
    A a {1};
    CHECK(a.value == 1);
}

TEST_CASE("A value direct assignement") {
    A a {1};
    a.value = 2;
    CHECK(a.value == 2);  // cppcheck-suppress knownConditionTrueFalse
}
