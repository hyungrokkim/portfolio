#include <typeinfo>
template<typename T, T* value1> struct only {
    only(): value(value1) {}
    only(T const& obj) {
        if(&obj == value1) value = value1;
        else throw std::bad_cast();
    }
    only(only const& obj): value(new T(*obj.value)) {}
    only& operator=(T const& obj) {
        if(&obj == value1) value = value1;
        else throw std::bad_cast();
        return *this;
    }
    only& operator=(only const& obj) {
        value=obj.value->clone(); return *this;
    }
    operator T() { return *value; }
private:
    T* value;
};
