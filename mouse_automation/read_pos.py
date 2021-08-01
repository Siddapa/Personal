import keyboard
from keyboard import mouse
import time


end_hour = '11'
end_minute = '5'


positions = []
with open('mouse_automation/pos.txt', 'r') as f:
    positions_str = f.readline()
    positions = positions_str.split(', ')[:-1]


print(time.ctime)
time.sleep(5)
while time.ctime[11:13] == end_hour and time.ctime[14:16] == end_minute:
    for i in range(0, len(positions), 2):
        mouse.move(positions[i], positions[i+1])
        mouse.click()
