#!/usr/bin/env python3
import unittest
from forge.led_bitmap_generator import generate_led_bitmap

class TestLedBitmapGenerator(unittest.TestCase):
    def test_generate_led_bitmap(self):
        bitmap = [[0, 1], [1, 0]]
        result = generate_led_bitmap(bitmap)
        self.assertEqual(result, 'Generated Bitmap')
