package FTC;

/**
 * Tracks position relative to starting location Currently uses motor encoders
 * for position feedback
 */
public class Odometry {
    public Wheel left_wheel;
    public Wheel right_wheel;
    private double imu;
    public double x, y;
    public double past_l, past_r;
    public final double TICKS = 4096;
    public final double CIRCUMFERENCE = 1.38 * Math.PI; // Inches
    final double h = 7.5; // Half-Width of the robot in ticks
    

    public Odometry(Wheel l_enc, Wheel r_enc){
        this.left_wheel = l_enc;
        this.left_wheel = r_enc;
        this.imu = 0;
    }

    /**
     * Updates overall x, y based on deltas from arc
     * x is forward/back and y is left/right
     */
    public void updateDeltas(){
        double radius, leg_x, leg_y, deltax, deltay, chord;
        double curr_l = getCurrentL();
        double curr_r = getCurrentR();
        double l = curr_l - past_l;
        double r = curr_r - past_r;
        double heading = Math.toRadians(imu);
        
        double dist = (l + r) / 2;

//        if (r > l){
//            radius = l / delta_heading;
//            leg_x = Math.cos(delta_heading) * (radius + h) - (radius + h);
//            leg_y = Math.sin(delta_heading * (radius + h));
//        } else if (l > r){
//            radius = r / delta_heading;
//            leg_x = (radius + h) - Math.cos(delta_heading) * (radius + h);
//            leg_y = Math.sin(delta_heading * (radius + h));
//        } else {
//            leg_x = Math.cos(delta_heading) * l;
//            leg_y = Math.sin(delta_heading) * l;
//        }
//
//        chord = Math.sqrt(Math.pow(leg_x, 2) + Math.pow(leg_y, 2));
//        deltax = chord * Math.sin(delta_heading);
//        deltay = chord * Math.cos(delta_heading);
        leg_x = Math.cos(heading) * dist;
        leg_y = Math.sin(heading) * dist;

        this.x += leg_x;
        this.y += leg_y;
        // heading += delta_heading;
        past_l = curr_l;
        past_r = curr_r;
    }

    public double getCurrentL(){
        return ticksToInches(left_wheel.getCurrentPosition());
    }

    public double getCurrentR(){
        return ticksToInches(right_wheel.getCurrentPosition());
    }

    public double ticksToInches(double ticks){
        double ratio = ticks / TICKS;
        return ratio * CIRCUMFERENCE;
    }

    public double inchesToTicks(double inches){
        double rotations = inches / CIRCUMFERENCE;
        return rotations * TICKS;
    }

    public void resetEncoders(){
        left_wheel.resetEncoders();
        right_wheel.resetEncoders();
    }

    public void setStartingPos(double start_y){
        this.x = -65;
        this.y = start_y;
    }

    public double getX(){
        return this.x;
    }

    public double getY(){
        return this.y;
    }

    public double getH(){
        return this.h;
    }
}
