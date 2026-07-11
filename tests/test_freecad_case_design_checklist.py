# This test checks the functionality of the FreeCAD case design checklist generator.

import unittest
from forge.freecad_case_design_checklist import generate_checklist

class TestFreeCADCaseDesignChecklist(unittest.TestCase):
    def test_generate_checklist(self):
        checklist = generate_checklist()
        self.assertEqual(len(checklist), 5)
        self.assertIn("Check dimensions", checklist)
        self.assertIn("Verify material properties", checklist)
        self.assertIn("Ensure proper ventilation", checklist)
        self.assertIn("Validate electrical connections", checklist)
        self.assertIn("Test for structural integrity", checklist)

if __name__ == '__main__':
    unittest.main()