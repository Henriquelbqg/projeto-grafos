
"""
Script para iniciar servidor HTTP local para visualizar os arquivos HTML gerados.
"""
import http.server
import socketserver
import os
from pathlib import Path

def main():

    out_dir = Path(__file__).parent / "out"
    os.chdir(out_dir)

    PORT = 8000

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"\nServidor HTTP iniciado!")
        print(f"Servindo arquivos de: {out_dir.absolute()}")
        print(f"\nAcesse os arquivos HTML em:")
        print(f"   • http://localhost:{PORT}/grafo_interativo.html")
        print(f"   • http://localhost:{PORT}/arvore_percurso.html")
        print(f"   • http://localhost:{PORT}/arvore_bfs_boa_vista.html")
        print(f"\nPressione Ctrl+C para parar o servidor\n")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServidor encerrado.")
            httpd.shutdown()

if __name__ == "__main__":
    main()
