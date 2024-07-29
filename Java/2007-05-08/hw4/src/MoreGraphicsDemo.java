/** A program to demonstrate the methods in the classes
 * RightTriangle, Rectangle, and Square. */

public class MoreGraphicsDemo {
    public static final int indent = 3; //offset
    public static final int triangleSide = 21;   //아랫 변의 길이
    public static final int side = 5;          //사각형의 세로길이
    public static final int bottom = 10;      //사각형의 가로길이
    
    public static void main(String[] args) {
        RightTriangle t1 = new RightTriangle(indent, triangleSide);
        Rectangle r1 = new Rectangle(indent, side, bottom);
        Square s1 = new Square(indent, side);
        
        t1.drawAt(1);
        System.out.println();
        System.out.println("Area of triangle = " + t1.area());
        System.out.println();
        System.out.println
                ("Circumference of triangle = " + t1.circumference());
        System.out.println();
        System.out.println("===============================");
        
        r1.drawAt(2);
        System.out.println("Area of rectangle = " + r1.area());
        System.out.println();
        System.out.println
                ("Circumference of rectangle = " + r1.circumference());
        System.out.println();
        System.out.println("===============================");
        
        s1.drawAt(3);
        System.out.println("Area of square = " + s1.area());
        System.out.println();
        System.out.println
                ("Circumference of square = " + s1.circumference());
        System.out.println();
        System.out.println("===============================");
        
    }
}