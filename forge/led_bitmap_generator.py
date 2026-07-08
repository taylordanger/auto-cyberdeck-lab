#!/usr/bin/env python3

import numpy as np

def generate_led_bitmap(width, height):
    bitmap = np.zeros((height, width), dtype=int)
    for y in range(height):
        for x in range(width):
            if (x + y) % 2 == 0:
                bitmap[y, x] = 1
    return bitmap

if __name__ == '__main__':
    bitmap = generate_led_bitmap(60, 9)
    print(bitmap)