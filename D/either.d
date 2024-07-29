module either;

class Either(A, B) {
    
    private A value1;
    private B value2;
    
    Either!(A, B) opAssign(Either!(A, B) obj)  {
        value1 = obj.value1;
        value2 = obj.value2;
    }
    
    Either!(A, B) opAssign(A obj) {
        value1 = obj;
        value2 = null;
    }
    
    Either!(A, B) opAssign(B obj) {
        value1 = null;
        value2 = obj;
    }
    
    bool is(T: A)() {
        return value1;
    }
    
    bool is(T: B)() {
        return value2;
    }
    
    A as(T: A)() {
        return value1;
    }
    
    A as(T: B)() {
        return value2;
    }

};
