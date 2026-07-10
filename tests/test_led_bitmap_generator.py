#!/usr/bin/env python3
import unittest
from forge import led_bitmap_generator

class TestLedBitmapGenerator(unittest.TestCase):
    def test_generate_led_bitmap(self):
        result = led_bitmap_generator.generate_led_bitmap('test')
        self.assertEqual(result, 'Generated Bitmap')
