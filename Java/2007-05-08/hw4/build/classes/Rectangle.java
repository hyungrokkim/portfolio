
/**
 * Filename: Rectangle.java
 * 
 * Class for rectangular box(일반적 사각형) to be drawn on screen.
 * Sides of the rectangle are specified in characters,
 * and, since each character is higher than it is wide,
 * these rectangles will look higher than you might expect.
 * 
 * Inherits getOffset, setOffset, and drawAt from Figure class.
 * Also has methods to calculate area and circumference.
 */

public class Rectangle extends Figure {
    private int height;
    private int width;
    
    public Rectangle() {
        
    }
    
    public Rectangle(int theOffset, int theHeight, int theWidth) {
        super(theOffset);
        height = theHeight;
        width = theWidth;
    }
    
    public void reset(int newOffset, int newHeight, int newWidth) {
        setOffset(newOffset);
        height = newHeight;
        width = newWidth;
    }
    
    // Draws the figure at the current line.
    public void drawHere() {
        drawHorizontalLine();
        drawSides();
        drawHorizontalLine();
    }
    
    private void drawHorizontalLine()   //가로변을 그림
    {
        spaces(getOffset());
        final char[] line = new char[width];
        java.util.Arrays.fill(line, '-');
        System.out.println(line);
    }
    
    
    //세로변을 모두 그림, drawOneLineOfSides() 이용
    private void drawSides(){
        for(int i: new int[height-2])
            drawOneLineOfSides();
    }
    
    private void drawOneLineOfSides()   //세로 변의 하나의 |       |를 그림
    {
        spaces(getOffset());
        System.out.print('|');
        spaces(width-2);
        System.out.println('|');
    }
    
    // Writes the indicated number of spaces.
    private static void spaces(int number) {
        final char[] chars = new char[number];
        java.util.Arrays.fill(chars, ' ');
        System.out.print(chars);
    }
    
    /**
     * Methods to calculate area and circumference.
     */
    public int area() {
        return (height * width);
    }
    
    public int circumference() {
        return (2 * height + 2 * width);
    }
}
