#!/usr/bin/env python3
import unittest
from forge import esp32_epaper_pinout

class TestESP32EpaperPinout(unittest.TestCase):
    def test_generate_pinout(self):
        pinout = esp32_epaper_pinout.generate_pinout()
        self.assertIn('GPIO0', pinout)
        self.assertEqual(pinout['GPIO0'], 'BOOTSTRAP')

if __name__ == '__main__':
    unittest.main()