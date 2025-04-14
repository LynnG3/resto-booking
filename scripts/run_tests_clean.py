#!/usr/bin/env python
"""
Запускает тесты и фильтрует вывод, показывая только результаты.
"""
import subprocess
import sys

def run_filtered_tests():
    """Запускает pytest и фильтрует вывод для чистоты."""
    # Запускаем тесты
    process = subprocess.run(
        ["pytest", "tests/", "-v", "--no-header", "-q"] + sys.argv[1:],
        capture_output=True,
        text=True
    )
    
    # Фильтруем вывод, оставляя только важные строки
    important_keywords = ["passed", "PASSED", "collected", "FAILED", "ERROR"]
    
    for line in process.stdout.split("\n"):
        if any(keyword in line for keyword in important_keywords):
            print(line)
    
    # Возвращаем тот же код завершения, что и pytest
    return process.returncode

if __name__ == "__main__":
    sys.exit(run_filtered_tests())
