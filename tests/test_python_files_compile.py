#!/usr/bin/env python3

import unittest
from forge.led_bitmap_generator import generate_led_bitmap

class TestLEDBitmapGenerator(unittest.TestCase):
    def test_generate_led_bitmap(self):
        bitmap = generate_led_bitmap()
        self.assertEqual(len(bitmap), 60)
        self.assertEqual(len(bitmap[0]), 9)

if __name__ == '__main__':
    unittest.main()