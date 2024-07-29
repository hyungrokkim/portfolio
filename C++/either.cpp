template<typename A, typename B> struct either {
    either(A const& obj): value_one(new A(obj)), value_two(0) {}
    either(B const& obj): value_one(0), value_two(new B(obj)) {}
    either(): value_one(new A), value_two(0) {}
    either(either<A,B> const& original):
        value_one(original.is<A>() ? new A(original.as<A>()) : 0),
        value_two(original.is<B>() ? new B(original.as<B>()) : 0) {}
    either<A,B>& operator=(either<A,B> const& original) {
        *this = (original.is<A>() ? original.as<A>() : original.as<B>() );
    }
    either& operator=(A const& obj) { this->~either(); value_one=new A(obj); }
    either& operator=(B const& obj) { this->~either(); value_two=new B(obj); }
    template<typename T> bool is() const { return match(static_cast<T*>(0)); }
    template<typename T> T& as() { return *match(static_cast<T*>(0)); }
    template<typename T> T const& as() const { return *match(static_cast<T*>(0)); }
private:
    std::auto_ptr<A> value_one;
    std::auto_ptr<B> value_two;
    A* match(A*) { return value_one; }
    B* match(B*) { return value_two; }
};
