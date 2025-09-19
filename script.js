document.addEventListener('DOMContentLoaded', () => {
  const horaSelect = document.getElementById('hora');
  const listaCitas = document.getElementById('listaCitas');
  const bookingForm = document.getElementById('bookingForm');
  const adminForm = document.getElementById('adminForm');

  // Rellenar horarios de 2pm a 5pm en intervalos de 15 minutos
  for (let h = 14; h <= 17; h++) {
    for (let m = 0; m < 60; m += 15) {
      const hora = `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}`;
      const option = document.createElement('option');
      option.value = hora;
      option.textContent = hora;
      horaSelect.appendChild(option);
    }
  }

  // Manejar agendar cita
  bookingForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const nombre = bookingForm.nombre.value;
    const fecha = bookingForm.fecha.value;
    const hora = bookingForm.hora.value;

    const cita = document.createElement('li');
    cita.textContent = `${fecha} ${hora} - ${nombre}`;
    listaCitas.appendChild(cita);

    bookingForm.reset();
  });

  // Validar modo admin
  adminForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const clave = adminForm.clave.value;
    if (clave === 'kikeadmin') {
      alert('Modo admin activado 💻');
    } else {
      alert('Clave incorrecta 🚫');
    }
    adminForm.reset();
  });
});
