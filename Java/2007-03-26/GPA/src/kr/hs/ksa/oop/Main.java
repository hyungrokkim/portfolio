package kr.hs.ksa.oop;

/**
 * Main class for GPA calculation application. Do not instantiate.
 * @author hk
 */
public class Main {
    
    private Main() {
    }
    
    /**
     * @param args the command line arguments
     */
    public static void main(final String... args) {
        final StudentReader studentReader = new StudentReader();
        new StudentListFormatter(new StudentReader().readStudents(5)).print();
    }
    
}
