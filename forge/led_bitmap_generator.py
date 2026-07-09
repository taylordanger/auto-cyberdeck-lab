#!/usr/bin/env python3

import numpy as np

LED_BITMAP_SIZE = (60, 9)

def generate_led_bitmap():
    bitmap = np.zeros(LED_BITMAP_SIZE, dtype=int)
    return bitmap.tolist()

if __name__ == '__main__':
    print(generate_led_bitmap())