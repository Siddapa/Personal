import numpy as np
import cv2 as cv
import time
import os
from threading import Thread
from subprocess import call


working_path = 'door_monitor/bins/'
new_img_filename = 'download.jpg'
new_img_path = '/mnt/flash_drive/' + new_img_filename


def display_image():
    executable_filename = 'displayable'
    call(['gcc', 'fast_gpio.c', '-o', executable_filename]) # Converts to executable
    call(['chmod', '+x', executable_filename]) # Changes permissions
    call(['./' + executable_filename]) # Prints to display
    call('rm', executable_filename) # Deletes executable


def img2bin():
    while 1:
        if True:
            red_bin = working_path + 'red.txt'
            green_bin = working_path + 'green.txt'
            blue_bin = working_path + 'blue.txt'
            img = cv.imread(working_path + new_img_filename)
            resized = cv.resize(img, (480, 272))
            with open(red_bin, 'w') as file:
                for row in resized:
                    for pixel in row:
                        true_value = int((pixel[0]/255) * 31) # Scales to 5-bit
                        binary = bin(true_value)
                        file.write(binary[2:]) # Removes '0b' part of binary literal

            with open(green_bin, 'w') as file:
                for row in resized:
                    for pixel in row:
                        true_value = int((pixel[1]/255) * 63) # Scales to 6-bit
                        binary = bin(true_value)
                        file.write(binary[2:]) # Removes '0b' part of binary literal

            with open(blue_bin, 'w') as file:
                for row in resized:
                    for pixel in row:
                        true_value = int((pixel[2]/255) * 31) # Scales to 5-bit
                        binary = bin(true_value)
                        file.write(binary[2:]) # Removes '0b' part of binary literal
        time.sleep(1)

if __name__ == "__main__":
    img_to_bin = Thread(target=img2bin)
    img_to_bin.start()