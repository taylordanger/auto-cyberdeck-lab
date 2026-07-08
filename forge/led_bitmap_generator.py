#!/usr/bin/env python3

def generate_led_bitmap(width, height):
    return [[0] * width for _ in range(height)]

if __name__ == '__main__':
    bitmap = generate_led_bitmap(60, 9)
    for row in bitmap:
        print(' '.join(str(pixel) for pixel in row))