#pragma once

#include <iostream>

class A {
public:
    A(int value);

    friend std::ostream & operator<<(std::ostream &,
            const A &);

private:
    int value;
};

std::ostream & operator<<(std::ostream &,
        const A &);
