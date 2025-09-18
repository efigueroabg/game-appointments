from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
CITAS_FILE = 'citas.json'
ADMIN_PASSWORD = 'kikeadmin'

# Generar horarios válidos de lunes a viernes de esta semana
def generar_horarios():
    horarios = []
    hoy = datetime.now()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    for i in range(5):  # Lunes a viernes
        dia = inicio_semana + timedelta(days=i)
        for h in range(14, 17):  # 2pm a 4:55pm
            for m in range(0, 60, 5):
                hora = f"{h:02d}:{m:02d}"
                horarios.append(f"{dia.strftime('%Y-%m-%d')} {hora}")
    return horarios

# Cargar citas desde archivo
def cargar_citas():
    if os.path.exists(CITAS_FILE):
        with open(CITAS_FILE, 'r') as f:
            return json.load(f)
    return {}

# Guardar citas en archivo
def guardar_citas(citas):
    with open(CITAS_FILE, 'w') as f:
        json.dump(citas, f, indent=2)

# Validar si usuario ya tiene cita ese día
def usuario_ya_agendado(nombre, fecha, citas):
    for horario, nombres in citas.items():
        if horario.startswith(fecha) and nombre in nombres:
            return True
    return False

@app.route('/')
def index():
    horarios = generar_horarios()
    citas = cargar_citas()
    citas_ordenadas = dict(sorted(citas.items(), key=lambda x: x[0]))
    return render_template('index.html', horarios=horarios, citas=citas_ordenadas)

@app.route('/agendar', methods=['POST'])
def agendar():
    nombre = request.form['nombre'].strip()
    horario = request.form['horario']
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
    return redirect('/')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        clave = request.form['clave']
        if clave == ADMIN_PASSWORD:
            citas = cargar_citas()
            citas_ordenadas = dict(sorted(citas.items(), key=lambda x: x[0]))
            return render_template('admin.html', citas=citas_ordenadas)
        else:
            return "Clave incorrecta."
    return render_template('admin_login.html')

@app.route('/borrar', methods=['POST'])
def borrar():
    horario = request.form['horario']
    citas = cargar_citas()
    if horario in citas:
        del citas[horario]
        guardar_citas(citas)
    return redirect('/admin')
