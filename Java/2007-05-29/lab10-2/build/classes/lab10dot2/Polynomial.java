package lab10dot2;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public final class Polynomial {
    private final List<Integer> coefficients;
    public Polynomial() {
        this(new DoublyLinkedList<Integer>());
    }
    public Polynomial(Integer... coefficients) {
        this(Arrays.asList(coefficients));
    }
    public Polynomial(List<Integer> coefficients) {
        this.coefficients = Collections.unmodifiableList(coefficients);
    }
    public Polynomial negate() {
        List<Integer> newCoefficients = new DoublyLinkedList<Integer>();
        for(Integer i: coefficients) newCoefficients.add(-i);
        return new Polynomial(newCoefficients);
    }
    public static Polynomial add(final Polynomial p1, final Polynomial p2) {
        List<Integer> newCoefficients = new DoublyLinkedList<Integer>();
        int i = 0;
        while(true) {
            if(Math.max(p1.coefficients.size(), p2.coefficients.size())
                    <= i) break;
            int i1 = p1.coefficients.size() > i ? p1.coefficients.get(i)
                    : 0;
            int i2 = p2.coefficients.size() > i ? p2.coefficients.get(i)
                    : 0;
            newCoefficients.add(i1 + i2);
            i++;
        }
        return new Polynomial(newCoefficients);
    }
    public static Polynomial subtract(final Polynomial p1, final Polynomial p2) {
        return add(p1, p2.negate());
    }
    @Override public String toString() {
        final StringBuilder builder = new StringBuilder();
        int count = 0;
        for(Integer i: coefficients) {
            if(count != 0) builder.append('+');
            builder.append(i);
            if(count != 0) builder.append("x^"+count);
            count++;
        }
        return builder.toString();
    }
}
