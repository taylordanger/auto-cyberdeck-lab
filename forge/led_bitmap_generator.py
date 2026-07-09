#!/usr/bin/env python3

import numpy as np
from PIL import Image

def generate_led_bitmap(width=60, height=9):
    # Create a blank image with white background
    bitmap = np.ones((height, width), dtype=np.uint8) * 255
    # Draw a black rectangle in the center
    x1, y1 = width // 4, height // 2 - 1
    x2, y2 = width * 3 // 4, height // 2 + 1
    bitmap[y1:y2+1, x1:x2+1] = 0
    # Save the image as a PNG file
    img = Image.fromarray(bitmap)
    img.save('led_bitmap.png')

if __name__ == '__main__':
    generate_led_bitmap()
