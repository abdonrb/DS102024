#!/usr/bin/env python
import subprocess
import sys
import os

def run_tests():
    """Ejecuta los tests y genera un informe de cobertura."""
    print("Ejecutando tests...")
    result = subprocess.run(["pytest", "--cov=utils", "--cov-report=term-missing"], capture_output=True, text=True)

    print("\nResultados de los tests:")
    print(result.stdout)

    if result.stderr:
        print("\nErrores:")
        print(result.stderr)

    return result.returncode

if __name__ == "__main__":
    # Cambiamos al directorio raíz del proyecto
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Ejecutamos los tests
    exit_code = run_tests()

    # Salimos con el código de retorno de pytest
    sys.exit(exit_code)
