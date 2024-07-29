module satisfies;

class Satisfies(T, bool function(T) predicate) {
    invariant {
        assert(predicate(obj));
    }
    
    private T value;
    
    this(T obj) {
        value = obj;
    }
    
    Satisfies!(T) opAssign(T obj) {
        value = obj;
    }
    
    T opCast() { return value; }
    
private:
    T value;
}


class Satisfies(T, bool delegate(T) predicate) {
    invariant {
        assert(predicate(obj));
    }
    
    private T value;
    
    this(T obj) {
        value = obj;
    }
    
    Satisfies!(T) opAssign(T obj) {
        value = obj;
    }
    
    T opCast() { return value; }
    
private:
    T value;
}