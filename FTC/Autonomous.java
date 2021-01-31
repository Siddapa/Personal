package FTC;

public class Autonomous{
    private Drivetrain drivetrain;
    private int step = -1;
    private Wheel left_wheel;
    private Wheel right_wheel;

    public Autonomous(){
        left_wheel = new Wheel();
        right_wheel = new Wheel();
        this.drivetrain = new Drivetrain(new Odometry(left_wheel, right_wheel));
    }

    public void start(){
        while (true){
            switch (step){
                case 0:
                drivetrain.setTargetPos(20);
                
                case 1:
                drivetrain.setTargetTurn(90);
            }
        }
    }

    public void update(){
        step = drivetrain.autoPIDUpdate();
        left_wheel.updateCurrentPosition();
        right_wheel.updateCurrentPosition();
        System.out.println(left_wheel.getCurrentPosition());
        System.out.println(right_wheel.getCurrentPosition());
    }
}