#!/usr/bin/env python3
import unittest
from forge import led_bitmap_generator

class TestLedBitmapGenerator(unittest.TestCase):
    def test_generate_led_bitmap(self):
        self.assertEqual(led_bitmap_generator.generate_led_bitmap('test'), 'test')

if __name__ == '__main__':
    unittest.main()
