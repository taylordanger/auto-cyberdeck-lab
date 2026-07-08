#!/usr/bin/env python3

import unittest
from forge.led_bitmap_generator import generate_led_bitmap

class TestLEDBitmapGenerator(unittest.TestCase):
    def test_generate_led_bitmap(self):
        img = generate_led_bitmap()
        self.assertEqual(img.size, (60, 9))
        self.assertTrue(isinstance(img, Image.Image))

if __name__ == '__main__':
    unittest.main()