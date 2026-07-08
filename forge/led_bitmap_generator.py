#!/usr/bin/env python3

import numpy as np
from PIL import Image

def generate_led_bitmap(width=60, height=9):
    bitmap = np.zeros((height, width), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            if (x + y) % 2 == 0:
                bitmap[y, x] = 255
    return Image.fromarray(bitmap)

if __name__ == '__main__':
    img = generate_led_bitmap()
    img.save('led_bitmap.png')