#include <typeinfo>
template<typename T, bool (*predicate)(T)> struct satisfies {
    satisfies(T const& obj) {
        if(!predicate(obj)) throw std::bad_cast();
        value = obj;
    }
    satisfies(satisfies const& obj): value(obj.value) {}
    satisfies& operator=(T const& obj) {
        if(!predicate(obj)) throw std::bad_cast();
        value = obj; return *this;
    }
    satisfies& operator=(satisfies const& obj) {
        value=obj.value; return *this;
    }
    operator T() { return value; }
private:
    T value;
};
