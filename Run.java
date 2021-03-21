public class Run{
    public static void test(double heading){
        double x_dist = -72 - 48;
        double y_dist = -55 - -48;

        // calculate target heading
        // CCW for imu is positive
        double robot_heading = heading % 360;
        if (Math.abs(robot_heading) > 180){
            robot_heading = (180 - Math.abs((robot_heading % 180))) * -Math.signum(robot_heading);
        }
        double test_heading = Math.toDegrees(Math.atan2(y_dist, x_dist));
        double turret_heading = robot_heading + (180 - Math.abs(test_heading)) * Math.signum(test_heading);
        System.out.println(turret_heading);

        double offset = turret_heading / 360.0;
        double rotation_pos = -0.413 + offset;
        System.out.print(rotation_pos);
    }


    public static void main(String[] args) {
        int[] blah = new int[]{0, 90, 180, 360, 450, -90, -180, -360, -450};
        int increment = 0;
        for(int item: blah){
            System.out.print(increment + ": ");
            test(item);
            System.out.println();
            increment++;
        }
    }
}