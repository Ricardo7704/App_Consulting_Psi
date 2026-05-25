# App de Citas Médicas - Consultas Psicológicas

Aplicación web simple para agendar citas médicas sin necesidad de base de datos. Los datos se guardan en el navegador (localStorage) y se envían confirmaciones por correo electrónico.

## ✨ Características

- **Agendar citas**: Formulario completo con RUT, nombre, edad, género, celular y email
- **Calendario dinámico**: Muestra próximos 5 días hábiles (lunes-viernes) con números reales
- **Navegación de semanas**: Avanza y retrocede entre semanas (mínimo semana actual)
- **Bloqueo automático**: Los horarios agendados desaparecen del calendario
- **Código de anulación**: Cada cita recibe un código único para cancelarla
- **Cancelación de citas**: Panel para ingresar código y liberar horarios
- **Confirmación por email**: Envía automáticamente confirmación y código de anulación
- **Sin base de datos**: Todo funciona con localStorage (navegador)

## 📋 Requisitos

- Python 3.7 o superior
- Gmail con autenticación de dos factores habilitada
- Navegador web moderno

## 🚀 Instalación

### 1. Preparar credenciales de Gmail

1. Ve a [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Selecciona "Correo" y "Windows Computer"
3. Google generará una contraseña de 16 caracteres (ej: `abcd efgh ijkl mnop`)
4. Copia esta contraseña

### 2. Configurar archivo .env

1. Copia el archivo `.env.example` y renómbralo a `.env`
2. Abre `.env` y rellena con tus datos:
```
GMAIL_EMAIL=tu_email@gmail.com
GMAIL_PASSWORD=abcd efgh ijkl mnop
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

O si tienes problemas de permisos:

```bash
pip install -r requirements.txt --break-system-packages
```

## 🎯 Uso

### Opción 1: Solo frontend (sin envío de correos)

1. Abre el archivo `app_citas_medicas.html` en tu navegador
2. Las citas se guardarán en localStorage
3. Los correos NO se enviarán

### Opción 2: Con backend completo (con envío de correos)

1. Abre PowerShell en esta carpeta
2. Ejecuta:
```bash
python enviar_correo.py
```
3. El servidor iniciará en `http://localhost:5000`
4. Abre el navegador en esa dirección
5. Presiona Ctrl+C en PowerShell para detener el servidor

## 📧 Estructura del correo

El cliente recibe un correo con:
- Confirmación de cita agendada
- Detalles completos (nombre, RUT, edad, género, celular)
- Día y hora de la cita
- **Código de anulación** único (para cancelar)
- Fecha de registro

## 🔒 Seguridad

- ✅ Las credenciales están en `.env` (protegido por `.gitignore`)
- ✅ El archivo `.env` nunca se sube a GitHub
- ✅ Las contraseñas NO se guardan en el código
- ✅ Usa SMTP SSL (puerto 465) para conexión segura

## 📁 Estructura de archivos

```
app_citas_medicas_v1_final/
├── app_citas_medicas.html      # App principal (HTML/CSS/JS)
├── enviar_correo.py             # Backend Flask
├── requirements.txt             # Dependencias Python
├── .env                         # Credenciales (NO subir a Git)
├── .env.example                 # Template
├── .gitignore                   # Protección de seguridad
└── README.md                    # Este archivo
```

## 🐛 Solución de problemas

### "ModuleNotFoundError: No module named 'flask'"
```bash
pip install flask flask-cors python-dotenv --break-system-packages
```

### "Error de autenticación de Gmail"
- Verifica que usaste la contraseña de aplicación (16 caracteres), no tu contraseña normal
- Activa autenticación de dos factores en tu cuenta Google
- Regenera la contraseña de aplicación

### Los correos no llegan
- Revisa spam/basura
- Verifica que `.env` esté correctamente configurado
- Asegúrate de que el servidor esté ejecutándose

## 📝 Notas

- Los datos se guardan en el navegador (localStorage)
- Si limpias el caché, se pierden las citas
- Cada cita tiene un código único de cancelación de 14 caracteres
- El calendario muestra solo días hábiles (lunes-viernes)
- No puedes agendar para días pasados

## 📞 Contacto

Para reportar problemas o sugerencias, contacta a rhamuy@gmail.com

---

**Versión**: 1.0 Final  
**Última actualización**: Mayo 2026
