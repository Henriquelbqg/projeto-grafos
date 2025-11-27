
"""
Comando único para gerar TODOS os arquivos da Parte 1 e visualizar os HTMLs.

Uso: python3 visualizar.py
"""
import subprocess
import sys
from pathlib import Path

def main():
    parte1_dir = Path(__file__).parent

    print("Gerando TODOS os arquivos da Parte 1...")
    print("=" * 60)


    result = subprocess.run(
        [sys.executable, "-m", "src.cli", "--serve"],
        cwd=parte1_dir
    )

    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
