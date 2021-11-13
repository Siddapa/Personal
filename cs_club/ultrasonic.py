import RPi.GPIO as g
from time import sleep, time


trig = 0
echo = 0

# Setup and reset trigger
g.setmode(g.BCM)
g.setup(trig, g.OUT)
g.setup(echo, g.IN)
g.output(trig, False)


# Send 10 mircosecond burst
g.output(trig, True)
sleep(0.00001)
g.output(trig, False)

# Calculate round-trip time
while g.input(echo) == 0:
    pulse_start = time()
while g.input(echo) == 1:
    pulse_end = time()

# Convert to distance
pulse_duration = pulse_start-pulse_end
distance = round(pulse_duration * 17150, 2)

print(distance)
