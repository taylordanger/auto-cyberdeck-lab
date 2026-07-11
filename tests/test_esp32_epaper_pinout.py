import unittest
from forge import esp32_epaper_pinout

class TestESP32EpaperPinout(unittest.TestCase):
    def test_get_pinout(self):
        pinout = esp32_epaper_pinout.get_pinout()
        self.assertIsInstance(pinout, dict)
        self.assertIn('VCC', pinout)
        self.assertIn('GND', pinout)

if __name__ == '__main__':
    unittest.main()