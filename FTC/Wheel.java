package ftc;

public class Wheel {
    private double power;
    private double ticks;
    private long past_time;

    public Wheel(){
        this.power = 0;
        this.ticks = 0;
        this.past_time = 0;
    }

    public void resetEncoders(){
        ticks = 0;
    }

    public double getCurrentPosition(){
        return ticks;
    }

    public void updateCurrentPosition(){
        ticks = power * (System.nanoTime() - past_time);
        past_time = System.nanoTime();
    }

    public void setPower(double power){
        this.power = power;
    }
}
