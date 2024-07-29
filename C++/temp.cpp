#include <cstdlib>
#include <stdexcept>
#include <iostream>
#include <ostream>
#include <cassert>
#include "either.cpp"
struct a {};
struct b {};


int main() {
    either<a, b> var;
    var=a();
    std::getchar();
}
