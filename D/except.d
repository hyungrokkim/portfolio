module except;

class Except(A) {
    Except!(A) opAssign(T)(T obj)
    in {
        assert(!(cast(A) obj))
    } body {
        value = new Holder!(T)(obj);
    }
    
    Except!(A) opAssign(Except!(A) obj) {
        value = obj.value.clone();
        return this;
    }
    
    T as(T)() {
        return (cast(Holder!(T)) value).value;
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
