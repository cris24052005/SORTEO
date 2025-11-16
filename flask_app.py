# app.py (Versión Final)
import os
import random
import threading
from flask import Flask, render_template, request

app = Flask(__name__)

file_lock = threading.Lock()

# Premios y probabilidades
PREMIOS = [
    "Pizza personal",
    "Pizza mediana",
    "Pizza grande",
    "Vaso de jugo",
    "Vaso de chicha",
    "Gelatina",
    "Postre",
    "Empanada",
    "Papa Rellena",
    "Tamal",
    "Cena",
    "Tajada de queque",
    "Gaseosa 500ml",
    "Gaseosa 1L"
]
PROBABILIDADES = [7,6,6,7,8,8,7,7,7,7,7,8,8,7]  # Suma 100

# ---------------------------
# Funciones auxiliares
# ---------------------------

def es_codigo_valido(codigo):
    try:
        with open('codigos_validos.txt', 'r') as f:
            for linea in f:
                if linea.strip().upper() == codigo:
                    return True
        return False
    except FileNotFoundError:
        print("ERROR: No existe codigos_validos.txt")
        return False

def es_codigo_usado(codigo):
    try:
        with open('codigos_usados.txt', 'r') as f:
            for linea in f:
                if linea.strip().upper() == codigo:
                    return True
        return False
    except FileNotFoundError:
        return False

def marcar_codigo_como_usado(codigo):
    with file_lock:
        try:
            with open('codigos_usados.txt', 'a') as f:
                f.write(codigo + "\n")
        except Exception as e:
            print("ERROR al escribir:", e)

# ---------------------------
# Rutas
# ---------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sortear', methods=['POST'])
def sortear():
    codigo_usuario = request.form['codigo'].strip().upper()

    # Caso 1: Código inválido
    if not es_codigo_valido(codigo_usuario):
        return render_template('index.html', error="❌ El código ingresado no es válido.")

    # Caso 2: Código repetido
    if es_codigo_usado(codigo_usuario):
        return render_template('index.html', error="⚠️ Este código ya fue utilizado.")

    # Caso 3: Código correcto → sortear premio
    premio_ganado = random.choices(PREMIOS, weights=PROBABILIDADES, k=1)[0]

    # Marcar como usado
    marcar_codigo_como_usado(codigo_usuario)

    # Mostrar ruleta
    return render_template('resultado.html', premio_final=premio_ganado)

# ---------------------------
# Ejecución
# ---------------------------

if __name__ == '__main__':
    if not os.path.exists('codigos_usados.txt'):
        open('codigos_usados.txt', 'w').close()

    if not os.path.exists('codigos_validos.txt'):
        with open('codigos_validos.txt', 'w') as f:
            f.write("PROMO-001\nPROMO-002\n")

    app.run(host='0.0.0.0', port=5000, debug=True)
