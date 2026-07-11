# This is a test for the ESP32/e-paper pinout utility.
import unittest
from forge import esp32_epaper_pinout

class TestESP32EpaperPinout(unittest.TestCase):
    def test_get_pinout(self):
        pinout = esp32_epaper_pinout.get_pinout()
        self.assertIn('GPIO0', pinout)
        self.assertEqual(pinout['GPIO0'], 'Boot mode selection')

if __name__ == '__main__':
    unittest.main()
