module both;

class Both(A, B) {
    
    private A value1;
    private B value2;
    
    Both!(A, B) opAssign(T)(T obj) {
        value1 = obj;
        value2 = obj;
    }
    
    // Cf. No custom casts...
};
