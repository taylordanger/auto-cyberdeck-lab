#!/usr/bin/env python3
import unittest
from forge import esp32_epaper_pinout

class TestESP32EpaperPinout(unittest.TestCase):
    def test_get_esp32_epaper_pinout(self):
        pinout = esp32_epaper_pinout.get_esp32_epaper_pinout()
        self.assertEqual(pinout['GPIO0'], 'Reset')
        self.assertEqual(pinout['GPIO1'], 'Deep Sleep')
        self.assertEqual(pinout['GPIO2'], 'Boot Mode')
        self.assertEqual(pinout['GPIO4'], 'Busy')
        self.assertEqual(pinout['GPIO5'], 'CS')
        self.assertEqual(pinout['GPIO10'], 'DC')
        self.assertEqual(pinout['GPIO13'], 'MOSI')
        self.assertEqual(pinout['GPIO14'], 'CLK')
        self.assertEqual(pinout['GPIO15'], 'RST')

if __name__ == '__main__':
    unittest.main()
