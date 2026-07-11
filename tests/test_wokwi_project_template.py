#!/usr/bin/env python3
import unittest
from forge.wokwi_project_template import generate_wokwi_template

class TestWokwiProjectTemplate(unittest.TestCase):
    def test_generate_wokwi_template(self):
        template = generate_wokwi_template()
        self.assertEqual(template['project']['name'], 'New Wokwi Project')
        self.assertEqual(template['project']['description'], 'A template project for Wokwi')
        self.assertEqual(template['project']['parts'], [])

if __name__ == '__main__':
    unittest.main()
