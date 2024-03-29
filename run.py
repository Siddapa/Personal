from re import sub
import threading
from time import sleep
from typing import final
import keyboard
import sys
import cv2 as cv
from math import pi, sin, cos
from math import factorial as f
import random

from webcam.sockets import Server
from webcam.sockets import Client
from webcam.video import Camera


def run_server():
    server = Server('127.0.0.1', 54321)
    server.listen()


def capture_camera():
    camera = Camera(0, Client('127.0.0.1', 54321))
    camera.capture()


def halt():
    while 1:
        if keyboard.is_pressed('ctrl+c'):
            raise KeyboardInterrupt

def recover(st): 
    codes = {"ZERO":0,"ONE":1,"TWO":2,"THREE":3,"FOUR":4,"FIVE":5,"SIX":6,"SEVEN":7,"EIGHT":8,"NINE":9}
    final = ""
    jump_flag = False
    for index, char in enumerate(st):
        jump_flag = False
        for i in range(index, 6):
            if jump_flag == True:
                break
            tester = st[int(index): int(index) + int(i)]
            for key in codes.keys():
                accuracy = 0
                for test_char in tester:
                    if test_char in key:
                        accuracy += 1
                if accuracy == len(key):
                    final += str(codes[key])
                    jump_flag = True
    print(final)
    return final


def check_type():
    assembly = ''
    while not keyboard.is_pressed('c'):
        if keyboard.is_pressed('1'):
            assembly += '1'
        if keyboard.is_pressed('2'):
            assembly += '2'
        if keyboard.is_pressed('3'):
            assembly += '3'
        if keyboard.is_pressed('4'):
            assembly += '4'
    print(assembly)



def detect_color():
    vid = cv.VideoCapture(0)
    ret, frame = vid.read()
    cv.imshow('Frame', frame)

    cv.blur(frame, )


def binomial_distribution(choices, prob_success, prob_failure):
    probs = []
    for i in range(choices + 1):
        perms = f(choices)/(f(i) * f(choices - i))
        prob = perms * prob_success**(i) * prob_failure**(choices - i)
        probs.append(prob)
    return probs


def brute_force():
    x = 0
    theta = 0.0
    max_area = 0
    final_x = 0
    final_theta = 0
    for i in range(0, 1500):
        for j in range(0, 9000):
            rads = theta * pi / 180.0
            area = 30 * sin(rads) - 2 * sin(rads) * cos(rads) * x**2
            if area > max_area:
                max_area = area
                final_theta = theta
                final_x = x
            theta += 0.01
        x += 0.01
        theta = 0
        print(x)
    print(max_area)
    print(final_theta)
    print(final_x)


def longestCommonPrefix(strs) -> str:
    prefix = ''
    if len(strs) == 1:
        return ''
    for index, char in enumerate(strs[0]):
        if len(char) == 0:
            return ''
        prefix += char
        for word in strs:
            if word[0:index + 1] != prefix:
                if len(prefix) == 1:
                    return ''
                print(prefix)
                return prefix[0:index]


def roman_to_int(input):
    symbols = {
        'I' : 1,
        'V' : 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    final_num = 0

    for index, char in enumerate(input):
        previous_num = symbols[input[index - 1]]
        curr_num = symbols[char]

        if index != 0:
            if previous_num < curr_num:
                final_num += curr_num - previous_num
            else:
                print(char)
                final_num += symbols[char]
        else:
            final_num += symbols[char]
    
    print(final_num)


def sid():
    total = 0
    for i in range(17, 24):
        total += 50/(f(i)*f(50-i))
    total *= 2
    total += 50/(f(25)*f(25))
    total /= 2
    print(total)


def budy(row):
    for i in range(row):
        printable = [' ' for j in range(row)]
        index = int(((row - 1) / 2) + 1)
        for j in range(i):
            printable[index + j] = '.'
        print(printable)


def has_repeating(test: str):
    for index, i in enumerate(test):
        try:
            blah = test[index + 1:].index(i)
            return True
        except ValueError:
            continue
    return False


def repeating_string(substring: str, pointer: int, size: int):
    print(substring[pointer:pointer + size])
    if has_repeating(substring[pointer:pointer + size]):
        if pointer + size == len(substring):
            repeating_string(substring, 0, size - 1)
        else:
            pointer += 1
    return size


def wordle():
    guessing = True
    words = ["Gene_symbol", "Validated", "Supported", "Approved", "Uncertain"]

    correct_word = words[random.randint(0, len(words) - 1)]
    print(correct_word)
    guess = input('Guess: ')

    while guessing:
        guess = input('Try Again: ')
        if guess.lower() == correct_word.lower():
            print('Correct')
            break
        continue


def typingtest():
    sleep(3)
    test = 'child world look not develop however leave day course change consider good man how ask word keep which give course school under mean like could this such would lead and nation large see may'
    for i in test:
        keyboard.press(i)
        sleep(0.03)


if __name__ == '__main__':
    # roman_to_int("MCMXCIV")
    # budy(5)
    # test = "abcabcbb"
    # blah = repeating_string(test, 0, len(test))
    # print(blah)
    # wordle()
    typingtest()