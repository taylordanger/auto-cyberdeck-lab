#!/usr/bin/env python3

import unittest
from forge.led_bitmap_generator import generate_led_bitmap

class TestLEDBitmapGenerator(unittest.TestCase):
    def test_generate_led_bitmap(self):
        # Call the function to generate the bitmap
        generate_led_bitmap()
        # Check if the image file is created
        self.assertTrue(os.path.exists('led_bitmap.png'))

if __name__ == '__main__':
    unittest.main()