

template<typename T> struct is {
    template<typename B>
    is(either<T, B> const& obj): value(obj.value_one) {}
    template<typename A>
    is(either<A, T> const& obj): value(obj.value_two) {}
    operator bool() { return value; }
private:
    void*& value;
};

template<typename T> struct as {
    template<typename B>
    as(either<T, B> const& obj): value(obj.value_one) {}
    template<typename A>
    as(either<A, T> const& obj): value(obj.value_two) {}
    operator T() { return *value; }
private:
    T*& value;
};
