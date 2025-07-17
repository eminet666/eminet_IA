import os
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Si le chemin correspond à un répertoire (dossier des images)
        if self.path.startswith("/dataset/train/"):
            self.send_image_list(self.path)
        else:
            # Autres requêtes servent les fichiers statiques (HTML, JS, etc.)
            super().do_GET()

    def send_image_list(self, path):
        # Vérifie si le dossier existe
        local_path = os.path.join(os.getcwd(), path.lstrip('/'))  # Retirer le '/' au début du chemin pour éviter l'erreur
        if os.path.isdir(local_path):
            # Liste les fichiers dans le répertoire
            files = [f for f in os.listdir(local_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(files).encode('utf-8'))
        else:
            self.send_error(404, "Directory not found")

if __name__ == "__main__":
    PORT = 8000
    handler = MyHandler
    httpd = HTTPServer(('', PORT), handler)
    print(f"Server started on port {PORT}")
    httpd.serve_forever()
