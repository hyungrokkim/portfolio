/**
 Class for square box(정사각형) to be drawn on screen.
 Sides of the square are specified in characters,
 and, since each character is higher than it is wide,
 these squares will look higher than you might expect.

 Inherits getOffset, setOffset, and drawAt from Figure class, 
 Inherits reset, drawHere, area and circumference from Rectangle class.
*/
public class Square extends Rectangle
{
    // instance variable 없음
    public Square()
    {
    
    }

    public Square(int theOffset, int theSide) //정사각형의 면적구함
    {
        super(theOffset, theSide, theSide);
    }

    //square의 instance variable들(Rectangle로부터 상속받은 것 )을 reset한다. 
    public void reset(int newOffset, int newSide) 
    {
        super.reset(newOffset, newSide, newSide);
    }
}

