# This is a test for the hardware inventory template generator.
import unittest
from forge.hardware_inventory_template import generate_hardware_inventory

class TestHardwareInventoryTemplate(unittest.TestCase):
    def test_generate_hardware_inventory(self):
        inventory = generate_hardware_inventory()
        self.assertEqual(len(inventory), 1)
        self.assertIn('Part Number', inventory[0])
        self.assertIn('Description', inventory[0])
        self.assertIn('Quantity', inventory[0])
        self.assertIn('Supplier', inventory[0])
        self.assertIn('Price', inventory[0])

if __name__ == '__main__':
    unittest.main()