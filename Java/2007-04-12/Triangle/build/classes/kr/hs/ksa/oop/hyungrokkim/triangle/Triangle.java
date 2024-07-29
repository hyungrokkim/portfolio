package kr.hs.ksa.oop.hyungrokkim.triangle;

/**
 * A triangle whose corners are points with integral coordinates.
 * @author Hyungrok Kim
 */
public class Triangle implements java.io.Serializable, Cloneable {
    public Triangle() {
        this(Point.ORIGIN, Point.ORIGIN, Point.ORIGIN);
    }
    
    @java.beans.ConstructorProperties({"p1", "p2", "p3"})
    public Triangle(final Point p1, final Point p2, final Point p3) {
        setP1(p1);
        setP2(p2);
        setP3(p3);
    }
    
    private Point p1, p2, p3;
    
    public void move(final int deltaX, final int deltaY, final int deltaZ) {
        setP1(getP1().moveX(deltaX).moveY(deltaY).moveZ(deltaZ));
        setP2(getP2().moveX(deltaX).moveY(deltaY).moveZ(deltaZ));
        setP3(getP3().moveX(deltaX).moveY(deltaY).moveZ(deltaZ));
    }
    
    public void printTriangle() {
        System.out.println(this);
    }
    
    @Override public String toString() {
        return "Triangle(" + getP1() + ", " + getP2() + ", " + getP3() + ")";
    }
    
    @Override public Triangle clone() {
        try {
            return (Triangle) super.clone();
        } catch (final CloneNotSupportedException ex) {
            throw new AssertionError(ex);
        }
    }
    
    /**
     * Immutable 3-dimensional point with integral coordinates.
     */
    public static final class Point
            implements java.io.Serializable, Cloneable {
        
        public static final Point ORIGIN = new Point();
        
        public Point() {
            this(0, 0, 0);
        }
        
        @java.beans.ConstructorProperties({"x", "y", "z"})
        public Point(final int x, final int y, final int z) {
            this.x = x;
            this.y = y;
            this.z = z;
        }
        
        private final int x;
        private final int y;
        private final int z;

        public int getX() {
            return x;
        }

        public int getY() {
            return y;
        }

        public int getZ() {
            return z;
        }
        
        public Point moveX(final int deltaX) {
            return new Point(getX() + deltaX, getY(), getZ());
        }
        
        public Point moveY(final int deltaY) {
            return new Point(getX(), getY() + deltaY, getZ());
        }
        
        public Point moveZ(final int deltaZ) {
            return new Point(getX(), getY(), getZ() + deltaZ);
        }
        
        @Override public Point clone() {
            try {
                return (Point) super.clone();
            } catch (final CloneNotSupportedException ex) {
                throw new AssertionError(ex);
            }
        }
        
        @Override public String toString() {
            return "(" + getX() + ", " + getY() + ", " + getZ() + ")";
        }
        
        @Override public boolean equals(final Object o) {
            if(o instanceof Point) {
                final Point p = (Point) o;
                return p.getX() == getX() &&
                       p.getY() == getY() &&
                       p.getZ() == getZ();
            } else return false;
        }
        
        @Override public int hashCode() {
            return java.util.Arrays.hashCode
                    (new int[] { getX(), getY(), getZ() });
        }
    }

    public Point getP1() {
        return p1;
    }

    public void setP1(final Point p1) {
        if(p1 == null) throw new NullPointerException("null point");
        this.p1 = p1;
    }

    public Point getP2() {
        return p2;
    }

    public void setP2(final Point p2) {
        if(p2 == null) throw new NullPointerException("null point");
        this.p2 = p2;
    }

    public Point getP3() {
        return p3;
    }

    public void setP3(final Point p3) {
        if(p3 == null) throw new NullPointerException("null point");
        this.p3 = p3;
    }
    
    @Override public boolean equals(final Object o) {
        if(o instanceof Triangle) {
            final Triangle t = (Triangle) o;
            return t.getP1().equals(getP1()) &&
                   t.getP2().equals(getP2()) &&
                   t.getP3().equals(getP3());
        } else return false;
    }
    
    @Override public int hashCode() {
        return java.util.Arrays.hashCode
                (new Point[] {getP1(), getP2(), getP3()});
    }
}
