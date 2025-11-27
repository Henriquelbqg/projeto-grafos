import http.server
import socketserver
import webbrowser
from pathlib import Path
import os

PORT = 8080
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENTRY_PAGE = "/interface_grafica/index.html"


def main():
    os.chdir(PROJECT_ROOT)
    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        url = f"http://localhost:{PORT}{ENTRY_PAGE}"
        print(f"Servindo projeto em {url}")
        try:
            webbrowser.open(url)
        except Exception:
            pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nEncerrando servidor...")


if __name__ == "__main__":
    main()
