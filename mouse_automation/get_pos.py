import keyboard
from keyboard import mouse


positions = []
while 1:
    if keyboard.is_pressed('p'): 
        pos = mouse.get_position()
        if pos not in positions:
            positions.append(pos)
    if keyboard.is_pressed('space'):
        break

with open('mouse_automation/pos.txt', 'w+') as f:
    for pos in positions:
        for coord in pos:
            print(coord)
            f.write(f"{coord}, ") 
print(positions)  