# Aplicación de Citas Médicas - Instrucciones de Configuración

## ⚠️ IMPORTANTE - SEGURIDAD

**NUNCA** subas el archivo `.env` a GitHub. Las credenciales están protegidas en `.gitignore`.

## Requisitos Previos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

## Instalación

### 1. Instalar dependencias

Abre una terminal/consola en la carpeta del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

O instálalas manualmente:

```bash
pip install flask flask-cors python-dotenv
```

### 2. Configurar variables de entorno (SEGURO)

#### 2.1 Crear archivo `.env`

1. En la carpeta del proyecto, copia el archivo `.env.example` y renómbralo a `.env`
2. O crea un nuevo archivo llamado `.env` con:

```
GMAIL_EMAIL=tu_email@gmail.com
GMAIL_PASSWORD=xxxx xxxx xxxx xxxx
```

#### 2.2 Obtener contraseña de Gmail

Para que el servidor pueda enviar correos a través de tu cuenta de Gmail:

1. Ve a tu cuenta de Google: https://myaccount.google.com/
2. En el lado izquierdo, selecciona "Seguridad"
3. Desplázate hasta "Contraseñas de aplicaciones"
4. Selecciona:
   - Aplicación: **Correo**
   - Dispositivo: **Windows Computer** (o tu sistema operativo)
5. Google te generará una contraseña de 16 caracteres (ej: `txyz abcd efgh ijkl`)
6. **Copia esa contraseña**

#### 2.3 Completar el archivo `.env`

Abre el archivo `.env` y complétalo:

```
GMAIL_EMAIL=tu_email@gmail.com
GMAIL_PASSWORD=txyz abcd efgh ijkl
```

**⚠️ IMPORTANTE:**
- El archivo `.env` **NO se subirá a GitHub** (está en `.gitignore`)
- Cada usuario/servidor debe tener su propio `.env`
- **NUNCA compartas tu archivo `.env`**

## Ejecutar la Aplicación

### Paso 1: Iniciar el servidor Flask

En la terminal, navega a la carpeta del proyecto y ejecuta:

```bash
python enviar_correo.py
```

Deberías ver un mensaje similar a:

```
 * Running on http://localhost:5000
```

**Deja esta ventana abierta mientras usas la aplicación.**

### Paso 2: Abrir la aplicación web

En tu navegador, abre el archivo HTML:

```
app_citas_medicas.html
```

O simplemente haz doble clic en el archivo.

## Usando la Aplicación

1. **Llenar el formulario:**
   - Ingresa tu RUT
   - Ingresa tu nombre completo
   - Ingresa tu edad
   - Selecciona tu género
   - Ingresa tu correo electrónico

2. **Seleccionar horario:**
   - Haz clic en el horario deseado (se marcará en verde)
   - Verás la confirmación: "Cita seleccionada: [Día] a las [Hora]"

3. **Aceptar cita:**
   - Presiona el botón "Aceptar"
   - El servidor enviará un correo de confirmación a tu correo electrónico
   - El horario desaparecerá de la lista (se marcará como no disponible)

4. **Confirmación:**
   - Recibirás un mensaje de éxito en la app
   - Verifica tu correo electrónico para la confirmación

## Solución de Problemas

### "El correo no llega"

1. **Verifica que el servidor está corriendo**
   - Deberías ver un mensaje en la terminal con `* Running on http://localhost:5000`

2. **Revisa la carpeta de Spam/Promociones**
   - Los correos a veces van a estas carpetas

3. **Verifica la contraseña de aplicación**
   - Asegúrate de haber copiado correctamente los 16 caracteres (incluyendo espacios)
   - No uses tu contraseña normal de Gmail, usa la contraseña de aplicación

4. **Errores en la consola del navegador**
   - Presiona F12 en el navegador
   - Ve a la pestaña "Console"
   - Verifica si hay mensajes de error

### "Error de conexión"

- Asegúrate que el servidor Python está corriendo
- Verifica que no hay otro programa usando el puerto 5000

### "Error de autenticación"

- La contraseña de aplicación es incorrecta
- Verifica que copiaste correctamente todos los 16 caracteres

## 🔐 Subir a GitHub de forma segura

### Archivos que SÍ se suben a GitHub:
- ✅ `app_citas_medicas.html`
- ✅ `enviar_correo.py`
- ✅ `.gitignore` (protege `.env`)
- ✅ `.env.example` (muestra qué configurar)
- ✅ `requirements.txt` (dependencias)
- ✅ `INSTRUCCIONES.md`
- ✅ `README.md`

### Archivos que NO se suben (bloqueados por `.gitignore`):
- ❌ `.env` (contiene credenciales)
- ❌ `__pycache__/`
- ❌ `venv/`

### Pasos para GitHub:

1. **Inicializar git:**
```bash
git init
git add .
git commit -m "Initial commit - App de citas médicas segura"
git remote add origin https://github.com/tu_usuario/tu_repo.git
git branch -M main
git push -u origin main
```

2. **Para otros usuarios (o tu en otra máquina):**
```bash
git clone https://github.com/tu_usuario/tu_repo.git
cd tu_repo
pip install -r requirements.txt
cp .env.example .env
# Edita .env con tus credenciales
python enviar_correo.py
```

## Archivos incluidos

- `app_citas_medicas.html` - Aplicación web (abre en navegador)
- `enviar_correo.py` - Servidor Flask para enviar correos (seguro)
- `.env` - Credenciales (NO se sube a GitHub)
- `.env.example` - Plantilla de configuración
- `.gitignore` - Protege archivos sensibles
- `requirements.txt` - Dependencias de Python
- `INSTRUCCIONES.md` - Este archivo

## Notas importantes

- El servidor debe estar corriendo mientras usas la aplicación
- Los horarios agendados se guardan en el navegador (localStorage)
- Si limpias los datos del navegador, se borrará el historial de citas
- El servidor usa cifrado SSL/TLS para conectarse a Gmail (puerto 465)

## Soporte

Si tienes problemas, verifica:
1. Que Python está instalado: `python --version`
2. Que Flask está instalado: `pip list | grep flask`
3. Que la contraseña de aplicación es correcta
4. Que el servidor está corriendo sin errores

¡Éxito!
