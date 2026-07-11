#!/usr/bin/env python3
import unittest
from forge import esp32_epaper_pinout

class TestESP32EpaperPinout(unittest.TestCase):
    def test_get_pinout(self):
        pinout = esp32_epaper_pinout.get_pinout()
        self.assertIn('GPIO0', pinout)
        self.assertEqual(pinout['GPIO0'], 'Input')

if __name__ == '__main__':
    unittest.main()