# 📅 Portal de Reservas Clínicas en Psicología

Aplicación web para agendar y cancelar citas médicas en consultas psicológicas. Incluye validación de horarios, envío de correos de confirmación y interfaz responsive para móviles.

## ✨ Características

- ✅ **Agendar citas**: Formulario completo con validación
- ✅ **Cancelar citas**: Búsqueda por código de anulación con confirmación
- ✅ **Correos automáticos**: Confirmación y notificaciones
- ✅ **Validación de horarios**: Previene citas duplicadas
- ✅ **Interfaz responsive**: Optimizada para móviles, tablets y desktop
- ✅ **Filtrado de horarios**: Oculta horas pasadas del día actual
- ✅ **Base de datos**: SQLite para persistencia

## 🚀 Tecnologías

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Base de datos**: SQLite
- **Email**: SMTP Gmail
- **Deployment**: Render

## 📋 Requisitos

- Python 3.11+
- pip (gestor de paquetes Python)

## 🔧 Instalación Local

1. **Clonar el repositorio:**
```bash
git clone <tu-repositorio-github>
cd "Consultas Psicologicas"
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno:**
Crear archivo `.env`:
```
GMAIL_EMAIL=tu_email@gmail.com
GMAIL_PASSWORD=xxxx xxxx xxxx xxxx
```

⚠️ **Importante**: La contraseña debe ser una "Contraseña de aplicación" de Gmail, no tu contraseña regular.

5. **Ejecutar la aplicación:**
```bash
python enviar_correo.py
```

Acceder a: `http://localhost:5000`

## 📱 Uso

### Agendar Cita
1. Completa el formulario con tus datos
2. Selecciona el día y hora disponible
3. Recibe confirmación por correo

### Anular Cita
1. Ve a la pestaña "Anular Cita"
2. Ingresa tu código de anulación
3. Confirma la anulación

## 🌐 Deployment en Render

1. Subir a GitHub (ver guía en proyecto)
2. Crear cuenta en Render
3. Conectar repositorio GitHub
4. Configurar variables de entorno
5. Deploy automático

## 📧 Configuración Gmail

1. Ve a [myaccount.google.com](https://myaccount.google.com)
2. Seguridad → Verificación en 2 pasos (habilitar)
3. Seguridad → Contraseñas de aplicación
4. Selecciona Correo y Windows
5. Copia la contraseña generada (16 caracteres)
6. Pega en `.env` como `GMAIL_PASSWORD`

## 📝 Estructura del Proyecto

```
Consultas Psicologicas/
├── enviar_correo.py          # Backend Flask
├── app_citas_medicas.html    # Frontend
├── requirements.txt          # Dependencias Python
├── .env                      # Variables de entorno (no subir a GitHub)
├── .gitignore               # Archivos a ignorar
├── Procfile                 # Configuración para Render
├── runtime.txt              # Versión de Python
└── README.md                # Este archivo
```

## 🐛 Solución de Problemas

**Error de autenticación Gmail:**
- Verifica que usaste "Contraseña de aplicación"
- No uses tu contraseña regular de Gmail

**Error de conexión a BD:**
- Asegúrate de tener permisos de escritura en la carpeta
- En Render, la BD se crea automáticamente

**App lenta en Render:**
- Planes gratuitos pueden ser lentos
- Considera plan pago para mejor rendimiento

## 📄 Licencia

Proyecto personal - Libre para uso y modificación.

## 👨‍💻 Autor

Desarrollado para Consultas Psicológicas

---

¿Preguntas? Contacta al desarrollador.
