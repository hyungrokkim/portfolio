module any;

class Any {
    
    Any opAssign(T)(T obj) {
        value = new Holder!(T)(obj);
        return this;
    }
    
    Any opAssign(Any obj) {
        value = obj.value.clone();
        return this;
    }
    
    T as(T)() {
        return (cast(Holder!(T)) value).value;
    }
    
    bool is(T)() {
        return cast(Holder!(T)) value;
    }
    
    private interface Clonable {
        Clonable clone();
    }
    
    private class Holder(T): Clonable {
        this(T value) {
            this.value = value;
        }
        private T value;
        override Holder!(T) clone() {
            return new Holder!(T)(value);
        }
    }
    
    private Clonable value;

};
