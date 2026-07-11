#!/usr/bin/env python3
import unittest
from forge.wokwi_project_template import generate_wokwi_template

class TestWokwiProjectTemplate(unittest.TestCase):
    def test_generate_wokwi_template(self):
        template = generate_wokwi_template("Test Project")
        self.assertEqual(template["name"], "Test Project")
        self.assertEqual(template["components"], [])
        self.assertEqual(template["connections"], [])

if __name__ == '__main__':
    unittest.main()
