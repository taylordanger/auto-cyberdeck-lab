#!/usr/bin/env python3

import subprocess
import os

def test_python_files_compile():
    result = subprocess.run(['python3', '-m', 'compileall', '.'], capture_output=True, text=True)
    assert result.returncode == 0, f'Compilation failed: {result.stderr}'

if __name__ == '__main__':
    test_python_files_compile()
