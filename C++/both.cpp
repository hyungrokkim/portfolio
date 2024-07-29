template<typename A, typename B> struct both {
    template<typename T> both(T const& obj): value_one(obj), value_two(obj) {}
    template<typename T> both& operator=(T const& obj) { return *this=both(obj); }
    operator A() const { return value_one; }
    operator B() const { return value_two; }
private:
    A value_one;
    B value_two;
};
