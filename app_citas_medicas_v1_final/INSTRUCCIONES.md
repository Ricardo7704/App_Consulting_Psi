# 📖 INSTRUCCIONES DE USO - App de Citas Médicas

## Paso 1: Obtener contraseña de Gmail

Para que la app pueda enviar correos, necesitas una **contraseña de aplicación especial** de Google.

### Pasos:
1. Abre [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) en tu navegador
2. Debe estar logueado con tu cuenta de Gmail
3. En "Selecciona la app", elige **Correo**
4. En "Selecciona el dispositivo", elige **Windows Computer**
5. Google generará una contraseña de **16 caracteres** (ejemplo: `abcd efgh ijkl mnop`)
6. **Copia esa contraseña** (con los espacios)

## Paso 2: Configurar el archivo .env

1. En la carpeta `app_citas_medicas_v1_final/`, busca el archivo `.env.example`
2. **Cópialo** y **renómbralo a `.env`** (sin la palabra "example")
3. Abre el archivo `.env` con un editor de texto (Bloc de notas)
4. Edita las líneas:
   ```
   GMAIL_EMAIL=tu_email@gmail.com
   GMAIL_PASSWORD=abcd efgh ijkl mnop
   ```
   Reemplaza:
   - `tu_email@gmail.com` con tu correo de Gmail
   - `abcd efgh ijkl mnop` con la contraseña que generaste en Paso 1

5. **Guarda el archivo** (Ctrl+S)

⚠️ **IMPORTANTE**: Nunca compartas el archivo `.env`. Está protegido en `.gitignore`

## Paso 3: Instalar dependencias

Abre PowerShell en la carpeta `app_citas_medicas_v1_final/` y ejecuta:

```powershell
pip install -r requirements.txt
```

Si sale error, intenta:
```powershell
pip install -r requirements.txt --break-system-packages
```

## Paso 4: Ejecutar la aplicación

### Con envío de correos (recomendado):

1. Abre PowerShell en la carpeta del proyecto
2. Ejecuta:
   ```powershell
   python enviar_correo.py
   ```
3. Deberías ver:
   ```
   ✅ Servidor configurado correctamente
   📧 Email: tu_email@gmail.com
   🔐 Contraseña: [Protegida en .env]

   * Running on http://localhost:5000
   Press CTRL+C to quit
   ```
4. Abre tu navegador en: **http://localhost:5000**
5. ¡La app está lista para usar!

### Sin envío de correos (solo prueba):

Simplemente abre el archivo `app_citas_medicas.html` en tu navegador.

## Paso 5: Usar la aplicación

### Para agendar una cita:

1. Completa el formulario:
   - RUT
   - Nombre Completo
   - Edad
   - Género (dropdown)
   - Celular (se agrega automáticamente +56)
   - Correo Electrónico

2. En el calendario, selecciona:
   - Una semana (botones "← Anterior" / "Siguiente →")
   - Un día y hora disponibles

3. Haz click en **"Aceptar"**

4. Se muestra un mensaje de confirmación

5. Si configuraste Gmail correctamente, el cliente recibe un correo con:
   - Confirmación de cita
   - **Código de Anulación** (importante: para cancelar luego)

### Para anular una cita:

1. Haz click en la pestaña **"❌ Anular Cita"**
2. Ingresa el **código de anulación** que recibiste por correo
3. Haz click en **"Anular Cita"**
4. El horario queda disponible nuevamente

## 📊 Características principales

| Característica | Estado |
|---|---|
| Agendar citas | ✅ |
| Calendario dinámico | ✅ |
| Mostrar solo días futuros | ✅ |
| Bloqueo de horarios | ✅ |
| Código de anulación | ✅ |
| Envío de correos | ✅ |
| Base de datos | ❌ (usa localStorage) |
| Autenticación | ❌ (sin login) |

## 🆘 Errores comunes y soluciones

### Error 1: "ModuleNotFoundError: No module named 'flask'"

**Solución:**
```powershell
pip install flask flask-cors python-dotenv
```

### Error 2: "Error de autenticación. Verifica la contraseña"

**Solución:**
- ¿Usaste la contraseña de APLICACIÓN (16 caracteres) o tu contraseña normal?
- Debe ser la contraseña de aplicación generada en Paso 1
- Regenera una nueva en [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

### Error 3: "No se envía el correo"

**Soluciones:**
1. Verifica que el archivo `.env` esté configurado correctamente
2. Revisa que el servidor esté corriendo (no cierres PowerShell)
3. Comprueba spam/basura del correo
4. Asegúrate de tener conexión a internet

### Error 4: "El calendario no muestra los días correctamente"

**Solución:**
- Actualiza el navegador con **Ctrl+F5** (limpiar caché)
- Cierra completamente el navegador y abrelo de nuevo

## 💾 Datos

- Las citas se guardan en **localStorage** del navegador
- No necesita base de datos
- Si limpias el caché del navegador, se pierden las citas
- Los datos son locales, no se envían a un servidor (excepto correos)

## 🔐 Seguridad

✅ Las credenciales está en `.env` (protegido)  
✅ La contraseña no aparece en el código  
✅ Usa conexión segura (SMTP SSL)  
✅ El `.env` está en `.gitignore` (no se sube a Git)  

## 📱 Requisitos de navegador

- Chrome
- Firefox
- Edge
- Safari
- Cualquier navegador moderno

## ❓ Preguntas frecuentes

**P: ¿Se guardan los datos en un servidor?**  
R: No. Todo está en el navegador (localStorage). Solo los correos se envían a través de Gmail.

**P: ¿Puedo ejecutar esto sin Gmail?**  
R: Sí, pero sin envío de correos. Abre directamente `app_citas_medicas.html`

**P: ¿Qué pasa si cierro PowerShell?**  
R: El servidor se detiene. Necesitas ejecutar el comando de nuevo para reactivarlo.

**P: ¿Puedo compartir el .env?**  
R: NO. Nunca compartas el `.env`. Contiene tus credenciales.

**P: ¿Cómo puedo compartir el código en GitHub?**  
R: El `.gitignore` protege automáticamente el `.env`. Comparte todo menos ese archivo.

---

**¿Listo? ¡Comienza en el Paso 1!** 🚀
