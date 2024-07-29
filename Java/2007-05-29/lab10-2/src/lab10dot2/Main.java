package lab10dot2;

import java.util.List;
import java.util.Scanner;

public class Main {
    public static void main(String... args) {
        Scanner scanner1 = new Scanner(System.console().readLine(
                "Enter coefficients of p1 (space-delimited): "));
        List<Integer> c1 = new DoublyLinkedList<Integer>();
        while(scanner1.hasNextInt()) c1.add(scanner1.nextInt());
        
        Scanner scanner2 = new Scanner(System.console().readLine(
                "Enter coefficients of p2 (space-delimited): "));
        List<Integer> c2 = new DoublyLinkedList<Integer>();
        while(scanner2.hasNextInt()) c2.add(scanner2.nextInt());
        Polynomial p1 = new Polynomial(c1), p2 = new Polynomial(c2);
        System.out.println("p1="+p1);
        System.out.println("p2="+p2);
        if(Boolean.parseBoolean(System.console().readLine("Add? (true for add, false for subtract) "))) {
            System.out.println("p1+p2=" + Polynomial.add(p1, p2));
        } else {
            System.out.println("p1-p2=" + Polynomial.subtract(p1, p2));
        }
    }
}
