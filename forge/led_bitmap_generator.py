#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

def generate_led_bitmap(width=60, height=9):
    bitmap = np.zeros((height, width), dtype=int)
    for y in range(height):
        for x in range(width):
            if (x + y) % 2 == 0:
                bitmap[y, x] = 1
    return bitmap

def plot_led_bitmap(bitmap):
    plt.imshow(bitmap, cmap='gray', interpolation='nearest')
    plt.show()

if __name__ == '__main__':
    bitmap = generate_led_bitmap()
    plot_led_bitmap(bitmap)