package kr.hs.ksa.oop.hyungrokkim.triangle;

/**
 *
 * @author hk
 */
public class Main {
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        final Triangle t = new Triangle();
        System.out.println(t);
        t.move(3, 4, 5);
        System.out.println(t);
    }
}
