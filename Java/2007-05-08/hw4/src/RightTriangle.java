/**
 * Class for right triangle to be drawn on screen. For this class,
 * a triangle points up and is completely determined by the size of
 * its base. The height is made equal to its base to accommodate
 * screen character spacing.  The triangle is printed with the
 * vertical side first.
 * Also has methods to calculate area and circumference.
 * Inherits getOffset, setOffset, and drawAt from Figure class,
 */
public class RightTriangle extends Figure {
    private int base;
    
    public RightTriangle() {
        
    }
    
    public RightTriangle(int theOffset, int theBase) {
        super(theOffset);
        base=theBase;
    }
    
    public void reset(int newOffset, int newBase) {
        setOffset(newOffset);
        base=newBase;
    }
    
    //  Draws the figure at current line.
    public void drawHere() {
        drawTop();
        drawBase();
    }
    
    private void drawBase()      //삼각형의 아랫 변을 그림
    {
        spaces(getOffset());
        final char[] baseEdge = new char[base];
        java.util.Arrays.fill(baseEdge, '*');
        System.out.println(baseEdge);
    }
    
    private void drawTop()      //삼각형의 왼쪽 세로 변과 빗변을 그림
    {
        spaces(getOffset());
        System.out.println('*');
        for(int i = 0; i < base-2; i++) {
            spaces(getOffset());
            System.out.print('*');
            spaces(i);
            System.out.println('*');
        }
    }
    
    private static void spaces(int number) {
        final char[] chars = new char[number];
        java.util.Arrays.fill(chars, ' ');
        System.out.print(chars);
    }
    
    // Methods to calculate area and circumference.
    public double area() {
        return base*base/2.;
    }
    
    //둘레길이 계산  square root : Math.sqrt(x)를 이용하시오.
    public double circumference(){
        return (2+Math.sqrt(2))*base;
    }
}