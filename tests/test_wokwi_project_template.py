import unittest
from templates.wokwi_project_template import generate_wokwi_project

class TestWokwiProjectTemplate(unittest.TestCase):
    def test_generate_wokwi_project(self):
        name = "Test Project"
        description = "A test project for Wokwi.",
        project = generate_wokwi_project(name, description)
        self.assertEqual(project['name'], name)
        self.assertEqual(project['description'], description)
        self.assertEqual(project['components'], [])
        self.assertEqual(project['connections'], [])

if __name__ == '__main__':
    unittest.main()