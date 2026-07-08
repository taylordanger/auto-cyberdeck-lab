import py_compile
from pathlib import Path
import unittest


class PythonCompileTests(unittest.TestCase):
    def test_forge_python_files_compile(self):
        repo_root = Path(__file__).resolve().parents[1]
        python_files = sorted((repo_root / "forge").glob("*.py"))

        self.assertTrue(python_files, "Expected at least one Python file in forge/")

        for path in python_files:
            with self.subTest(path=str(path)):
                py_compile.compile(str(path), doraise=True)


if __name__ == "__main__":
    unittest.main()
