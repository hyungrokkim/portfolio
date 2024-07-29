template<typename A> struct except {
    except(): value(new holder<int>(0)) {}
    template<typename T> except(T const& obj): value(new holder<T>(obj)) {}
    except(A const&);
    except(except<A> const& obj): value(obj.value->clone()) {}
    template<typename T> except& operator=(T const& obj) {
        delete value; value=new holder<T>(obj); return *this;
    }
    except<A>& operator=(except<A> const& obj) {
        delete value; value=obj.value->clone(); return *this;
    }
    except<A>& operator=(A const&);
    ~except() { delete value; }
    template<typename T>
    T& as() { return dynamic_cast<holder<T>*>(value)->value; }
    template<typename T>
    T const& as() const { return dynamic_cast<holder<T>*>(value)->value; }
private:
    struct holder_base { virtual ~holder_base() {} virtual holder_base* clone(); };
    holder_base* value;
    template<typename T> struct holder: holder_base {
        holder(T const& obj): value(obj) {}
        T value;
        holder<T>* clone() { return new holder<T>(value); }
    };
};
