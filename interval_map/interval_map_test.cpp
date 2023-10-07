#include "interval_map.hpp"

#include <catch2/catch_all.hpp>

template <typename Key, typename Value>
class Interval_map_test: public Interval_map<Key, Value> {
public:
    using Interval_map<Key, Value>::Interval_map;

    const std::map<Key, Value> & get_internal_map() const {
        return Interval_map<Key, Value>::map;
    }
};

TEST_CASE("empty map") {
    Interval_map<int, char> map {'z'};
    CHECK(map[0] == 'z');
}

TEST_CASE("invalid interval") {
    Interval_map_test<int, char> map {'z'};
    map.add_interval(1, 1, 'a');
    map.add_interval(2, 1, 'b');
    CHECK(map.get_internal_map().empty());
}

TEST_CASE("first interval") {
    Interval_map_test<int, char> map {'z'};
    map.add_interval(1, 10, 'a');
    const std::map<int, char> expected = {
            {1, 'a'},
            {10, 'z'}};
    CHECK(map.get_internal_map() == expected);
    CHECK(map[0] == 'z');
    CHECK(map[1] == 'a');
    CHECK(map[9] == 'a');
    CHECK(map[10] == 'z');
}

TEST_CASE("second non intersecting interval") {
    Interval_map_test<int, char> map {'z'};
    map.add_interval(1, 10, 'a');

    SECTION("before the first one") {
        map.add_interval(-20, -10, 'b');
        const std::map<int, char> expected = {
                {-20, 'b'},
                {-10, 'z'},
                {1, 'a'},
                {10, 'z'}};
        CHECK(map.get_internal_map() == expected);
        CHECK(map[-21] == 'z');
        CHECK(map[-20] == 'b');
        CHECK(map[-11] == 'b');
        CHECK(map[-10] == 'z');
        CHECK(map[0] == 'z');
        CHECK(map[1] == 'a');
        CHECK(map[9] == 'a');
        CHECK(map[10] == 'z');
    }

    SECTION("after the first one") {
        map.add_interval(20, 30, 'b');
        const std::map<int, char> expected = {
                {1, 'a'},
                {10, 'z'},
                {20, 'b'},
                {30, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }
}

TEST_CASE("second adjacent interval") {
    Interval_map_test<int, char> map {'z'};
    map.add_interval(1, 10, 'a');

    SECTION("before the first one") {
        map.add_interval(0, 1, 'b');
        const std::map<int, char> expected = {
                {0, 'b'},
                {1, 'a'},
                {10, 'z'}};
    }

    SECTION("after the first one") {
        map.add_interval(10, 20, 'b');
        const std::map<int, char> expected = {
                {1, 'a'},
                {10, 'b'},
                {20, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }
}

TEST_CASE("second intersecting interval") {
    Interval_map_test<int, char> map {'z'};
    map.add_interval(1, 10, 'a');

    SECTION("including the first one") {
        map.add_interval(0, 11, 'b');
        const std::map<int, char> expected = {
                {0, 'b'},
                {11, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("over the beginning of the first one") {
        map.add_interval(0, 5, 'b');
        const std::map<int, char> expected = {
                {0, 'b'},
                {5, 'a'},
                {10, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("over the end of the first one") {
        map.add_interval(5, 15, 'b');
        const std::map<int, char> expected = {
                {1, 'a'},
                {5, 'b'},
                {15, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("within the first one") {
        map.add_interval(2, 5, 'b');
        const std::map<int, char> expected = {
                {1, 'a'},
                {2, 'b'},
                {5, 'a'},
                {10, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("same as the first one") {
        map.add_interval(1, 10, 'b');
        const std::map<int, char> expected = {
                {1, 'b'},
                {10, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }
}

TEST_CASE("second intersecting interval with same value") {
    Interval_map_test<int, char> map {'z'};
    map.add_interval(1, 10, 'a');

    SECTION("over the beginning of the first one") {
        map.add_interval(0, 5, 'a');
        const std::map<int, char> expected = {
                {0, 'a'},
                {10, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("over the end of the first one") {
        map.add_interval(5, 15, 'a');
        const std::map<int, char> expected = {
                {1, 'a'},
                {15, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("within the first one") {
        map.add_interval(2, 5, 'a');
        const std::map<int, char> expected = {
                {1, 'a'},
                {10, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("adjacent before") {
        map.add_interval(0, 1, 'a');
        const std::map<int, char> expected = {
                {0, 'a'},
                {10, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("adjacent after") {
        map.add_interval(10, 11, 'a');
        const std::map<int, char> expected = {
                {1, 'a'},
                {11, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("same interval") {
        map.add_interval(1, 10, 'a');
        const std::map<int, char> expected = {
                {1, 'a'},
                {10, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }
}

TEST_CASE("two_consecutive_intervals") {
    Interval_map_test<int, char> map {'z'};
    map.add_interval(0, 10, 'a');
    map.add_interval(10, 20, 'b');

    SECTION("overlapping first interval") {
        map.add_interval(-5, 5, 'c');
        const std::map<int, char> expected = {
                {-5, 'c'},
                {5, 'a'},
                {10, 'b'},
                {20, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("overlapping second interval") {
        map.add_interval(15, 25, 'c');
        const std::map<int, char> expected = {
                {0, 'a'},
                {10, 'b'},
                {15, 'c'},
                {25, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("overlapping both intervals") {
        map.add_interval(5, 15, 'c');
        const std::map<int, char> expected = {
                {0, 'a'},
                {5, 'c'},
                {15, 'b'},
                {20, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("including both intervals") {
        map.add_interval(-5, 25, 'c');
        const std::map<int, char> expected = {
                {-5, 'c'},
                {25, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("same as both intervals") {
        map.add_interval(0, 20, 'c');
        const std::map<int, char> expected = {
                {0, 'c'},
                {20, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }
}

TEST_CASE("two non consecutive intervals") {
    Interval_map_test<int, char> map {'z'};
    map.add_interval(0, 10, 'a');
    map.add_interval(20, 30, 'b');

    SECTION("within both, non consecutive") {
        map.add_interval(11, 19, 'c');
        const std::map<int, char> expected = {
                {0, 'a'},
                {10, 'z'},
                {11, 'c'},
                {19, 'z'},
                {20, 'b'},
                {30, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("within both and consecutive") {
        map.add_interval(10, 20, 'c');
        const std::map<int, char> expected = {
                {0, 'a'},
                {10, 'c'},
                {20, 'b'},
                {30, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("overlapping both") {
        map.add_interval(5, 25, 'c');
        const std::map<int, char> expected = {
                {0, 'a'},
                {5, 'c'},
                {25, 'b'},
                {30, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("overlapping both and over first one") {
        map.add_interval(-5, 25, 'c');
        const std::map<int, char> expected = {
                {-5, 'c'},
                {25, 'b'},
                {30, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("overlapping both and over second one") {
        map.add_interval(5, 35, 'c');
        const std::map<int, char> expected = {
                {0, 'a'},
                {5, 'c'},
                {35, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("including both intervals") {
        map.add_interval(-5, 35, 'c');
        const std::map<int, char> expected = {
                {-5, 'c'},
                {35, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("merging with first interval") {
        map.add_interval(5, 15, 'a');
        const std::map<int, char> expected = {
                {0, 'a'},
                {15, 'z'},
                {20, 'b'},
                {30, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("merging with second interval") {
        map.add_interval(15, 25, 'b');
        const std::map<int, char> expected = {
                {0, 'a'},
                {10, 'z'},
                {15, 'b'},
                {30, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("overlapping first interval") {
        map.add_interval(5, 15, 'c');
        const std::map<int, char> expected = {
                {0, 'a'},
                {5, 'c'},
                {15, 'z'},
                {20, 'b'},
                {30, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("overlapping second interval") {
        map.add_interval(15, 25, 'c');
        const std::map<int, char> expected = {
                {0, 'a'},
                {10, 'z'},
                {15, 'c'},
                {25, 'b'},
                {30, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }
}

TEST_CASE("merging three intervals") {
    Interval_map_test<int, char> map {'z'};
    map.add_interval(0, 10, 'a');
    map.add_interval(20, 30, 'a');

    SECTION("adjacent") {
        map.add_interval(10, 20, 'a');
        const std::map<int, char> expected = {
                {0, 'a'},
                {30, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("overlapping") {
        map.add_interval(5, 25, 'a');
        const std::map<int, char> expected = {
                {0, 'a'},
                {30, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("including exactly") {
        map.add_interval(0, 30, 'a');
        const std::map<int, char> expected = {
                {0, 'a'},
                {30, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("including") {
        map.add_interval(-10, 40, 'a');
        const std::map<int, char> expected = {
                {-10, 'a'},
                {40, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }
}

TEST_CASE("merging four intervals") {
    Interval_map_test<int, char> map {'z'};
    map.add_interval(0, 10, 'a');
    map.add_interval(20, 30, 'a');
    map.add_interval(40, 50, 'a');

    SECTION("including") {
        map.add_interval(-10, 60, 'a');
        const std::map<int, char> expected = {
                {-10, 'a'},
                {60, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }
}

TEST_CASE("default value for first interval") {
    Interval_map_test<int, char> map {'z'};
    map.add_interval(0, 10, 'z');
    CHECK(map.get_internal_map().empty());
}

TEST_CASE("second interval using default value") {
    Interval_map_test<int, char> map {'z'};
    map.add_interval(0, 10, 'a');

    SECTION("before first interval adjacent") {
        map.add_interval(-1, 0, 'z');
        const std::map<int, char> expected = {
                {0, 'a'},
                {10, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("before first interval no adjacent") {
        map.add_interval(-10, -1, 'z');
        const std::map<int, char> expected = {
                {0, 'a'},
                {10, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("overlapping first interval below") {
        map.add_interval(-10, 5, 'z');
        const std::map<int, char> expected = {
                {5, 'a'},
                {10, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("after first interval adjacent") {
        map.add_interval(10, 11, 'z');
        const std::map<int, char> expected = {
                {0, 'a'},
                {10, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("after first interval non adjacent") {
        map.add_interval(20, 30, 'z');
        const std::map<int, char> expected = {
                {0, 'a'},
                {10, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("overlapping first interval above") {
        map.add_interval(5, 20, 'z');
        const std::map<int, char> expected = {
                {0, 'a'},
                {5, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }

    SECTION("including exactly whole first interval") {
        map.add_interval(0, 10, 'z');
        CHECK(map.get_internal_map().empty());
    }

    SECTION("including whole first interval") {
        map.add_interval(-10, 20, 'z');
        CHECK(map.get_internal_map().empty());
    }

    SECTION("within first interval") {
        map.add_interval(1, 9, 'z');
        const std::map<int, char> expected = {
                {0, 'a'},
                {1, 'z'},
                {9, 'a'},
                {10, 'z'}};
        CHECK(map.get_internal_map() == expected);
    }
}

TEST_CASE("third interval using default value") {
    Interval_map_test<int, char> map {'z'};
    map.add_interval(0, 10, 'a');

    SECTION("adjacent second interval") {
        map.add_interval(10, 20, 'b');

        SECTION("including exactly first interval") {
            map.add_interval(0, 10, 'z');
            const std::map<int, char> expected = {
                    {10, 'b'},
                    {20, 'z'}};
            CHECK(map.get_internal_map() == expected);
        }

        SECTION("including exactly second interval") {
            map.add_interval(10, 20, 'z');
            const std::map<int, char> expected = {
                    {0, 'a'},
                    {10, 'z'}};
            CHECK(map.get_internal_map() == expected);
        }

        SECTION("overlapping both") {
            map.add_interval(5, 15, 'z');
            const std::map<int, char> expected = {
                    {0, 'a'},
                    {5, 'z'},
                    {15, 'b'},
                    {20, 'z'}};
            CHECK(map.get_internal_map() == expected);
        }

        SECTION("including exactly both") {
            map.add_interval(0, 20, 'z');
            CHECK(map.get_internal_map().empty());
        }

        SECTION("including both") {
            map.add_interval(-10, 30, 'z');
            CHECK(map.get_internal_map().empty());
        }
    }

    SECTION("non adjacent second interval") {
        map.add_interval(20, 30, 'b');

        SECTION("between") {
            map.add_interval(11, 19, 'z');
            const std::map<int, char> expected = {
                    {0, 'a'},
                    {10, 'z'},
                    {20, 'b'},
                    {30, 'z'}};
            CHECK(map.get_internal_map() == expected);
        }

        SECTION("between exactly") {
            map.add_interval(10, 20, 'z');
            const std::map<int, char> expected = {
                    {0, 'a'},
                    {10, 'z'},
                    {20, 'b'},
                    {30, 'z'}};
            CHECK(map.get_internal_map() == expected);
        }

        SECTION("overlapping first") {
            map.add_interval(5, 15, 'z');
            const std::map<int, char> expected = {
                    {0, 'a'},
                    {5, 'z'},
                    {20, 'b'},
                    {30, 'z'}};
            CHECK(map.get_internal_map() == expected);
        }

        SECTION("overlapping second") {
            map.add_interval(15, 25, 'z');
            const std::map<int, char> expected = {
                    {0, 'a'},
                    {10, 'z'},
                    {25, 'b'},
                    {30, 'z'}};
            CHECK(map.get_internal_map() == expected);
        }

        SECTION("overlapping both") {
            map.add_interval(5, 25, 'z');
            const std::map<int, char> expected = {
                    {0, 'a'},
                    {5, 'z'},
                    {25, 'b'},
                    {30, 'z'}};
            CHECK(map.get_internal_map() == expected);
        }
    }
}

class Value {
public:
    explicit Value(char _v):
                v {_v} {
    }
    Value() = delete;
    Value(const Value &) = default;
    Value(Value &&) = default;
    Value & operator=(const Value &) = default;
    Value & operator=(Value &&) = default;

    bool operator==(const Value & other) const {
        return (v == other.v);
    }

    friend std::ostream & operator<<(std::ostream & os,
            const Value & value) {
        os << value.v;
        return os;
    }

private:
    char v;
};

class Key {
public:
    explicit Key(int _k):
                k {_k} {
    }
    Key() = delete;
    Key(const Key &) = default;
    Key(Key &&) = default;
    Key & operator=(const Key &) = default;
    Key & operator=(Key &&) = default;

    bool operator<(const Key & other) const {
        return (k < other.k);
    }

    friend std::ostream & operator<<(std::ostream & os,
            const Key & key) {
        os << key.k;
        return os;
    }

private:
    int k;
};

TEST_CASE("minimalist template classes") {
    SECTION("empty map") {
        Interval_map<Key, Value> map {Value {'z'}};
        CHECK(map[Key {0}] == Value {'z'});
    }

    SECTION("invalid interval") {
        Interval_map<Key, Value> map {Value {'z'}};
        map.add_interval(Key {1}, Key {1}, Value {'a'});
        map.add_interval(Key {2}, Key {1}, Value {'b'});
        CHECK(map[Key {1}] == Value {'z'});
    }

    SECTION("first interval") {
        Interval_map<Key, Value> map {Value {'z'}};
        map.add_interval(Key {1}, Key {10}, Value {'a'});
        CHECK(map[Key {0}] == Value {'z'});
        CHECK(map[Key {1}] == Value {'a'});
        CHECK(map[Key {9}] == Value {'a'});
        CHECK(map[Key {10}] == Value {'z'});
    }

    SECTION("two non consecutive intervals, third overlapping both") {
        Interval_map<Key, Value> map {Value {'z'}};
        map.add_interval(Key {0}, Key {10}, Value {'a'});
        map.add_interval(Key {20}, Key {30}, Value {'b'});
        map.add_interval(Key {5}, Key {25}, Value {'c'});
        CHECK(map[Key {-1}] == Value {'z'});
        CHECK(map[Key {0}] == Value {'a'});
        CHECK(map[Key {4}] == Value {'a'});
        CHECK(map[Key {5}] == Value {'c'});
        CHECK(map[Key {24}] == Value {'c'});
        CHECK(map[Key {25}] == Value {'b'});
        CHECK(map[Key {29}] == Value {'b'});
        CHECK(map[Key {30}] == Value {'z'});
    }
}
