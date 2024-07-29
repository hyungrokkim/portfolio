struct any {
    any(): value(new holder<int>(0)) {}
    template<typename T> any(T const& obj): value(new holder<T>(obj)) {}
    any(any const& obj): value(obj.value->clone()) {}
    template<typename T> any& operator=(T const& obj) {
        value=new holder<T>(obj); return *this;
    }
    any& operator=(any const& obj) {
        value=obj.value->clone(); return *this;
    }
    template<typename T>
    bool is() const { return dynamic_cast<holder<T>*>(value); }
    template<typename T>
    T& as() { return dynamic_cast<holder<T>&>(*value).value; }
    template<typename T>
    T const& as() const { return dynamic_cast<holder<T>&>(*value).value; }
private:
    struct holder_base { virtual ~holder_base() {} virtual holder_base* clone(); };
    std::auto_ptr<holder_base> value;
    template<typename T> struct holder: holder_base {
        holder(T const& obj): value(obj) {}
        T value;
        holder<T>* clone() { return new holder<T>(value); }
    };
};
