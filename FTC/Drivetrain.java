package ftc;

/**
 * Drivetrain -- handles movement of the drive wheels.
 */

public class Drivetrain {
    private Wheel left_wheel;
    private Wheel right_wheel;
    private Odometry odometry;
    private int auto_id = 0;
    public double l_target = 0;
    public double r_target = 0;
    boolean send_event = false;

    public Drivetrain(Odometry odometry){
        this.odometry = odometry;
    }

    public void resetEncoders(){
    }

    /**
     * Move the drivetrain based on gamepad-compatible inputs
     * @param left_stick_y Left Wheel Velocity
     * @param right_stick_y Right Wheel Velocity
     */
    public void telemove(double left_stick_y, double right_stick_y){
        //Subtracts power from forward based on the amount of rotation in the other stick
        double left_wheel_speed = -left_stick_y + right_stick_y;
        double right_wheel_speed = -left_stick_y - right_stick_y;
        left_wheel.setPower(left_wheel_speed);
        right_wheel.setPower(left_wheel_speed);
    }

    /**
     * Updates target distance in ticks
     * Appends to current position to account for previous movements
     * @param distance Desired distance in inches
     */
    public void setTargetPos(double distance){
        double target_ticks = odometry.inchesToTicks(distance);
        if (l_target != 0.0 && r_target != 0.0) {
            l_target = target_ticks + l_target;
            r_target = target_ticks + r_target;
        }
        send_event = true;
    }

    /**
     * Turns robot certain degrees
     * @param target_angle Range = 180 to -180 (counter-clockwise)
     */
    public void setTargetTurn(double target_angle){
        double target_ticks = odometry.getH() * target_angle;
        if (l_target != 0 && r_target != 0) {
            double direction = Math.signum(target_angle);
            l_target = direction * -target_ticks + l_target;
            r_target = direction * target_ticks + r_target;
        }
    }

    /**
     * Accelerates towards a set target positions for both wheels
     * Must be ran at the end of each loop cycle
     */
    public int autoPIDUpdate(){
        // TODO Find PID constant
        final double kP = 1;
        double l_error = l_target - left_wheel.getCurrentPosition();
        double r_error = r_target - right_wheel.getCurrentPosition();
        double left_wheel_speed = l_error * kP;
        double right_wheel_speed = r_error * kP;
        // TODO Increase deadband for error to make it possible to reach
        if (l_error > 10 || l_error < -10){
            left_wheel.setPower(left_wheel_speed);
            right_wheel.setPower(right_wheel_speed);
        } else {
            if (send_event){
                send_event = false;
                return auto_id + 1;
            }
        }
        return auto_id;
    }

    public Odometry getOdometry(){
        return this.odometry;
    }
}
