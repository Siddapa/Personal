import java.nio.ByteBuffer;

public class Run{
    public static void main(String[] args){
        ByteBuffer buf = ByteBuffer.allocate(44);
        buf.putDouble(10);
        buf.putDouble(20);
        buf.flip();
        System.out.println(buf);
    }
}