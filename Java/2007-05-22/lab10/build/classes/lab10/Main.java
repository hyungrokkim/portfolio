package lab10;

import java.util.Arrays;
import java.util.Vector;

public class Main {
    public static void main(final String[] args) {
        run(new Vector<Integer>());
    }
    public static void run(Vector<Integer> vector) {
            System.out.println(Arrays.toString(UserAction.values()));
            UserAction.valueOf(System.console().readLine("Enter choice: "))
                    .perform(vector);
            run(vector);
    }
}
