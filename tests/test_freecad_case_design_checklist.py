#!/usr/bin/env python3
import unittest
from forge.freecad_case_design_checklist import generate_checklist

class TestFreeCADCaseDesignChecklist(unittest.TestCase):
    def test_generate_checklist(self):
        checklist = generate_checklist()
        self.assertEqual(len(checklist), 4)
        self.assertIn("Check dimensions", checklist)
        self.assertIn("Verify material properties", checklist)
        self.assertIn("Ensure proper ventilation", checklist)
        self.assertIn("Test for structural integrity", checklist)

if __name__ == '__main__':
    unittest.main()
