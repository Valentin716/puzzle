from flask import Flask, send_file
import subprocess

app = Flask(__name__)

# Ruta para cargar la página web Frontend
@app.route('/')
def home():
    return send_file('index.html')

# Ruta que el botón de la web llama para ejecutar tu código
@app.route('/resolver')
def resolver_puzzle():
    # Asegúrate de que tu archivo original se llame 'BFS.py' o cambia el nombre aquí
    proceso = subprocess.run(['python', 'BFS.py'], capture_output=True, text=True)
    
    # Devuelve el texto exacto que imprimió tu archivo original
    return proceso.stdout

if __name__ == '__main__':
    app.run(port=5000, debug=True)  