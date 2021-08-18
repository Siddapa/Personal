import RPi.GPIO as g
import cv2 as cv
import time
import os
from threading import Thread
from subprocess import call
import RPi.GPIO as g


def display_image():
    executable_filename = 'displayable'
    g.setmode(g.BCM)
    g.setup(20, g.IN)
    img_counter = 0

    while 1:
        i = -1
        while os.path.isfile('bins/' + str(i) + 'red.txt'):
            i += 1
        if g.input(20):
            img_counter += 1
            if img_counter > i:
                img_counter = 0
            call(['gcc', 'pixel_data.c', '-o', executable_filename]) # Converts to executable
            call(['chmod', '+x', executable_filename]) # Changes permissions
            call(['sudo', './' + executable_filename, img_counter]) # Prints to display
        time.sleep(0.5)


def img2bin():
    img_counter = -1
    working_path = 'bins/' + str(img_counter + 1)
    while os.path.isfile(working_path + 'red.txt'):
        img_counter += 1

    new_img_filename = 'new_img.jpg'
    new_img_path = '/mnt/flash_drive/' + new_img_filename

    while 1:
        if os.path.isfile(new_img_path):
            red_bin = working_path + 'red.txt'
            green_bin = working_path + 'green.txt'
            blue_bin = working_path + 'blue.txt'
            img = cv.imread(new_img_path)
            resized = cv.resize(img, (480, 272))

            color_converted = cv.cvtColor(resized, cv.COLOR_BGR2RGB)
            with open(red_bin, 'w') as file:
                for row in color_converted:
                    for pixel in row:
                        true_value = int((pixel[0]/255) * 31) # Scales to 5-bit
                        binary = bin(true_value)
                        file.write(binary[2:]) # Removes '0b' part of binary literal

            with open(green_bin, 'w') as file:
                for row in color_converted:
                    for pixel in row:
                        true_value = int((pixel[1]/255) * 63) # Scales to 6-bit
                        binary = bin(true_value)
                        file.write(binary[2:]) # Removes '0b' part of binary literal

            with open(blue_bin, 'w') as file:
                for row in color_converted:
                    for pixel in row:
                        true_value = int((pixel[2]/255) * 31) # Scales to 5-bit
                        binary = bin(true_value)
                        file.write(binary[2:]) # Removes '0b' part of binary literal

            subprocess.run(['sudo', 'mv', '/mnt/flash_drive/' + new_img_filename, 'images/' + img_counter + new_img_filename])
            img_counter += 1
            print('Finished Converting')
        else:
            time.sleep(0.5)
            print('Waiting for Img')


if __name__ == "__main__":
    # PINOUT USAGE
    # Pins 0 to 15 for 16-bit color
    # 0-4 for Red (inclusive)
    # 5-10 for Green (inclusive)
    # 11-15 for Blue (inclusive)
    # 16 for Pic Switching

    img_to_bin = Thread(target=img2bin)
    display_img = Thread(target=display_image)
    display_img.start()
