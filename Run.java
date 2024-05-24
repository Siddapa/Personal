import java.nio.ByteBuffer;
import java.util.Arrays;
import java.util.List;

class Shape {
    public int x = 2;
    class Square {
        public int x = 3;

        public int hey(){
            return x;
        }
    }

    public int blah() {
        Square square = new Square();
        return square.hey();
    }

    public static void main(String[] args) {
        int n = 100;
        for (int i = n; i > 0; i /= (n-10)) {
            System.out.println(i);
            System.out.println(i / (n-10));
        }
    }
}