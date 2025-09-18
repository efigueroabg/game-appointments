from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
CITAS_FILE = "citas.json"
ADMIN_PASSWORD = "kikeadmin"

def cargar_citas():
    if os.path.exists(CITAS_FILE):
        with open(CITAS_FILE, "r") as f:
            citas = json.load(f)
        # Ordenar citas cronológicamente
        citas_ordenadas = dict(sorted(citas.items(), key=lambda x: x[0]))
        return citas_ordenadas
    return {}

def guardar_citas(citas):
    with open(CITAS_FILE, "w") as f:
        json.dump(citas, f, indent=4)

def generar_intervalos():
    hoy = datetime.now()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    intervalos = []
    for i in range(5):  # Lunes a viernes
        dia = inicio_semana + timedelta(days=i)
        hora = datetime(dia.year, dia.month, dia.day, 14, 0)
        while hora.hour < 17 or (hora.hour == 17 and hora.minute == 0):
            clave = hora.strftime("%Y-%m-%d %H:%M")
            intervalos.append(clave)
            hora += timedelta(minutes=5)
    return intervalos

@app.route("/")
def index():
    citas = cargar_citas()
    intervalos = generar_intervalos()
    return render_template("index.html", citas=citas, intervalos=intervalos)

@app.route("/agendar", methods=["POST"])
def agendar():
    nombre = request.form["nombre"]
    horario = request.form["horario"]
    citas = cargar_citas()
    if horario not in citas:
        citas[horario] = []
    if len(citas[horario]) < 2:
        citas[horario].append(nombre)
        guardar_citas(citas)
    return redirect("/")

@app.route("/admin", methods=["POST"])
def admin():
    clave = request.form["clave"]
    if clave == ADMIN_PASSWORD:
        citas = cargar_citas()
        return render_template("admin.html", citas=citas)
    return redirect("/")

@app.route("/borrar", methods=["POST"])
def borrar():
    horario = request.form["horario"]
    citas = cargar_citas()
    if horario in citas:
        del citas[horario]
        guardar_citas(citas)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
