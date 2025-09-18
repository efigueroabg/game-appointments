from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
ARCHIVO_CITAS = "citas.json"
ADMIN_CLAVE = "kikeadmin"

def generar_horarios():
    hoy = datetime.today()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    horarios = []
    for i in range(5):  # Lunes a viernes
        dia = inicio_semana + timedelta(days=i)
        fecha = dia.strftime("%Y-%m-%d")
        hora = datetime.strptime("14:00", "%H:%M")
        fin = datetime.strptime("17:00", "%H:%M")
        while hora <= fin:
            horarios.append(f"{fecha} {hora.strftime('%H:%M')}")
            hora += timedelta(minutes=15)
    return horarios

def cargar_citas():
    if os.path.exists(ARCHIVO_CITAS):
        with open(ARCHIVO_CITAS, "r") as f:
            return json.load(f)
    return {}

def guardar_citas(citas):
    with open(ARCHIVO_CITAS, "w") as f:
        json.dump(citas, f)

def usuario_ya_agendado(nombre, fecha, citas):
    for horario, nombres in citas.items():
        if horario.startswith(fecha) and nombre in nombres:
            return True
    return False

@app.route("/")
def index():
    horarios = generar_horarios()
    citas = cargar_citas()
    citas_ordenadas = dict(sorted(citas.items(), key=lambda x: x[0]))
    return render_template("index.html", horarios=horarios, citas=citas_ordenadas)

@app.route("/agendar", methods=["POST"])
def agendar():
    nombre = request.form["nombre"].strip()
    horario = request.form["horario"]
    if not nombre or not horario:
        return "Nombre y horario son requeridos."
    citas = cargar_citas()
    fecha = horario.split(" ")[0]
    if usuario_ya_agendado(nombre, fecha, citas):
        return "Ya tienes una cita agendada para ese día."
    if horario not in citas:
        citas[horario] = []
    if len(citas[horario]) >= 2:
        return "Este horario ya está lleno."
    citas[horario].append(nombre)
    guardar_citas(citas)
    return redirect("/")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        clave = request.form["clave"]
        if clave == ADMIN_CLAVE:
            citas = cargar_citas()
            citas_ordenadas = dict(sorted(citas.items(), key=lambda x: x[0]))
            return render_template("admin.html", citas=citas_ordenadas)
        else:
            return "Clave incorrecta."
    return render_template("admin_login.html")

@app.route("/borrar", methods=["POST"])
def borrar():
    horario = request.form["horario"]
    citas = cargar_citas()
    if horario in citas:
        del citas[horario]
        guardar_citas(citas)
    return redirect("/admin")

if __name__ == "__main__":
    app.run(debug=True)
