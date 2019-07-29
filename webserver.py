import http.server
import socketserver

with socketserver.TCPServer(("127.0.0.1",60030),http.server.SimpleHTTPRequestHandler) as httpd:
    httpd.serve_forever()

