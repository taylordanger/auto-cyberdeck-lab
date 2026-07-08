#!/usr/bin/env python3

import numpy as np
from PIL import Image

def generate_led_bitmap(width=60, height=9):
    # Create a blank image with white background
    img = Image.new('1', (width, height), 'white')
    pixels = img.load()

    # Draw some LEDs on the image
    for x in range(0, width, 5):
        for y in range(0, height, 2):
            pixels[x, y] = 'black'

    return img

if __name__ == '__main__':
    img = generate_led_bitmap()
    img.show()