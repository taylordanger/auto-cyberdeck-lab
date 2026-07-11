# Test for ESP32/e-paper pinout helper
import unittest
from forge import esp32_epaper_pinout
class TestESP32EpaperPinout(unittest.TestCase):
    def test_generate_pinout(self):
        self.assertEqual(esp32_epaper_pinout.generate_pinout(), "ESP32/e-paper pinout documentation")
