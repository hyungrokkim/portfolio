package kr.hs.ksa.picalculate;
import static java.lang.System.out;
import static java.lang.Math.abs;

public class Main {
    public static void main(String... args) {
        double a=0, b=1, c=0;
        for(int n=1;abs(b)>=1e-6;out.println("x["+n+"]="+
                (a+=(b=(n%2*8-4.)/(2*n++-1)))));
        for(int n=1;abs(a-b)>=1e-6;b=a,out.println("y["+n+"]="+(
                a=(c+=(n%2*8-4)/(2*n-1.))-(n%2*8-4)/(n+1./(2*n++-3)))));
    }
}
