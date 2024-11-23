import http.server
import socketserver
import os
PORT = 80
Handler = http.server.SimpleHTTPRequestHandler
os.chdir(os.path.dirname(os.path.abspath(__file__)))
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Сервер запущено на порту {PORT}")
    httpd.serve_forever()
