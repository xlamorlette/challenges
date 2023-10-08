#pragma once

#include <functional>
#include <iostream>
#include <map>

template <typename Key, typename Value>
class Interval_map {
public:
    explicit Interval_map(const Value & _default_value):
                default_value(_default_value) {
    }

    const Value & operator[](const Key & key) const {
        const auto it = map.upper_bound(key);
        if (it == map.cbegin()) {
            return default_value;
        } else {
            return std::prev(it)->second;
        }
    }

    /**
     * key_inf is inclusive, key_sup is exclusive
     */
    void add_interval(const Key & key_inf,
            const Key & key_sup,
            const Value & value) {
        if (! (key_inf < key_sup)) {
            return;
        }
        const auto it_key_inf = map.lower_bound(key_inf);
        const auto it_key_sup = map.upper_bound(key_sup);
        std::reference_wrapper<const Value> previous_value = std::cref(default_value);
        if (it_key_inf != map.cbegin()) {
            previous_value = std::cref(std::prev(it_key_inf)->second);
        }
        if (((it_key_inf == map.cbegin())
                    && (it_key_sup == map.cbegin()))
                || (it_key_sup == map.cend())) {
            map.erase(it_key_inf, it_key_sup);
            if (! (value == default_value)) {
                map.insert(it_key_sup, std::make_pair(key_sup, default_value));
            }
        } else {
            const Value & next_value = std::prev(it_key_sup)->second;
            if (! (value == next_value)) {
                map.insert(it_key_sup, std::make_pair(key_sup, next_value));
                if (it_key_sup != it_key_inf) {
                    map.erase(it_key_inf, std::prev(it_key_sup));
                }
            } else {
                map.erase(it_key_inf, it_key_sup);
            }
        }
        if (! (value == previous_value)) {
            map.insert(it_key_sup, std::make_pair(key_inf, value));
        }
    }

private:
    Value default_value;
    std::map<Key, Value> map;

    template <typename K, typename V>
    friend std::ostream & operator<<(std::ostream &,
            const Interval_map<Key, Value> &);

    template <typename K, typename V>
    friend class Interval_map_test;
};

template <typename Key, typename Value>
std::ostream & operator<<(std::ostream & os,
        const Interval_map<Key, Value> & map) {
    os << "-inf: " << map.default_value << std::endl;
    for (const auto & [key, value]: map.map) {
        os << key << ": " << value << std::endl;
    }
    return os;
}
