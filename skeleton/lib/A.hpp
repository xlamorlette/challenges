#pragma once

#include <iostream>

class A {
public:
    int value;

    explicit A(int value);

    friend std::ostream & operator<<(std::ostream &,
            const A &);
};

std::ostream & operator<<(std::ostream &,
        const A &);
