public class Run{

    public static void main(String[] args){
        String[] write_param = {"blah", "hello"};
        String trans = "";
        for (int i = 0; i < write_param.length; i++){
            trans += write_param[i] + " ";
        }
        System.out.println(trans);
    }
}