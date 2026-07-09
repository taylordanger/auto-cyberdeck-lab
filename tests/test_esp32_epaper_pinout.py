#!/usr/bin/env python3
import unittest
from forge.esp32_epaper_pinout import get_pinout

class TestESP32EpaperPinout(unittest.TestCase):
    def test_pinout(self):
        pinout = get_pinout()
        self.assertIn('GPIO0', pinout)
        self.assertEqual(pinout['GPIO0'], 'BOOTSTRAP')
        # Add more tests as needed

if __name__ == '__main__':
    unittest.main()