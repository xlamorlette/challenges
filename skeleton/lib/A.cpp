#include "A.hpp"

A::A(int value):
            value {value} {
}

std::ostream & operator<<(std::ostream & os,
        const A & a) {
    os << a.value;
    return os;
}
