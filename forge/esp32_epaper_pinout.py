#!/usr/bin/env python3

import sys

def print_pinout():
    print("ESP32 e-Paper Pinout")
    print("-------------------")
    print("GPIO 15: CS")
    print("GPIO 14: DC")
    print("GPIO 2: RST")
    print("GPIO 0: BUSY")

if __name__ == '__main__':
    print_pinout()