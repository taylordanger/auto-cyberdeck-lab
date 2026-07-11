import unittest
from templates import hardware_inventory_template

class TestHardwareInventoryTemplate(unittest.TestCase):
    def test_generate_template(self):
        template = hardware_inventory_template.generate()
        self.assertIsNotNone(template)
        self.assertIn('Part Number', template)
        self.assertIn('Quantity', template)

if __name__ == '__main__':
    unittest.main()