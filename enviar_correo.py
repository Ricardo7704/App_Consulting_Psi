from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
import threading
import traceback
import requests
import json

# Cargar variables de entorno desde archivo .env
load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Crear carpeta instance si no existe (para la BD)
instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
try:
    if not os.path.exists(instance_path):
        os.makedirs(instance_path, exist_ok=True)
except Exception as e:
    print(f"⚠️  Advertencia al crear carpeta instance: {e}")

# Configurar SQLite con ruta absoluta
db_path = os.path.join(instance_path, 'reservas.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

try:
    db = SQLAlchemy(app)
except Exception as e:
    print(f"❌ Error al inicializar la base de datos: {e}")
    raise

# Modelo de base de datos para reservas
class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(20), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(50), nullable=False)
    especialista = db.Column(db.String(100), nullable=False)
    celular = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    dia = db.Column(db.String(50), nullable=False)
    hora = db.Column(db.String(10), nullable=False)
    codigo_anulacion = db.Column(db.String(50), unique=True, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    estado = db.Column(db.String(20), default='activa')  # activa o anulada

    def to_dict(self):
        return {
            'id': self.id,
            'rut': self.rut,
            'nombre': self.nombre,
            'edad': self.edad,
            'genero': self.genero,
            'especialista': self.especialista,
            'celular': self.celular,
            'email': self.email,
            'dia': self.dia,
            'hora': self.hora,
            'codigo_anulacion': self.codigo_anulacion,
            'fecha_creacion': self.fecha_creacion.strftime('%d/%m/%Y %H:%M'),
            'estado': self.estado
        }

# Crear tablas
try:
    with app.app_context():
        db.create_all()
except Exception as e:
    print(f"⚠️  Advertencia al crear tablas de BD: {e}")

# Configuración de SendGrid (SEGURO - NO SE EXPONE EN GITHUB)
SENDER_EMAIL = os.getenv('GMAIL_EMAIL', '').strip()
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY', '').strip()

# Validar que las variables estén configuradas
if not SENDER_EMAIL:
    raise ValueError("Variable GMAIL_EMAIL no está configurada")
if not SENDGRID_API_KEY:
    raise ValueError("Variable SENDGRID_API_KEY no está configurada")

# Función para enviar email en un thread separado (asincrónico)
def enviar_email_async(destinatario, asunto, cuerpo_html, cuerpo_texto):
    """Envía email usando SendGrid API REST en un thread separado"""
    print(f"\n📧 Intentando enviar email a: {destinatario}")
    print(f"📧 Remitente: {SENDER_EMAIL}")
    print(f"📧 Asunto: {asunto}")
    print(f"📧 Usando SendGrid API REST")

    try:
        print("📧 Paso 1: Preparando payload...")
        # Construir payload para SendGrid - Solo texto plano
        payload = {
            "personalizations": [
                {
                    "to": [{"email": destinatario}],
                    "subject": asunto
                }
            ],
            "from": {
                "email": SENDER_EMAIL,
                "name": "Consultas Psicologicas - Sistema de Citas"
            },
            "replyTo": {
                "email": SENDER_EMAIL
            },
            "content": [
                {
                    "type": "text/plain",
                    "value": cuerpo_html
                }
            ],
            "headers": {
                "X-Priority": "3",
                "X-Mailer": "SendGrid/1.0",
                "Precedence": "list",
                "X-Entity-Ref-ID": f"appointment-{codigo_anulacion}",
                "List-Unsubscribe": "<mailto:noreply@consultas-psicologicas.com>"
            }
        }

        print("📧 Paso 2: Preparando headers...")
        headers = {
            "Authorization": f"Bearer {SENDGRID_API_KEY}",
            "Content-Type": "application/json"
        }

        print("📧 Paso 3: Enviando a SendGrid...")
        print(f"   - Timeout: 30 segundos")
        response = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers=headers,
            json=payload,
            timeout=30
        )

        print(f"📧 Paso 4: Respuesta recibida")
        print(f"   Status Code: {response.status_code}")

        if response.status_code == 202:
            print(f"✅ Email enviado exitosamente a {destinatario}\n")
        else:
            print(f"⚠️ SendGrid respondió: {response.text}\n")

    except requests.exceptions.Timeout:
        print(f"⏱️ TIMEOUT al enviar email a {destinatario}\n")

    except Exception as e:
        print(f"❌ ERROR al enviar email a {destinatario}: {str(e)}")
        print(f"❌ Tipo: {type(e).__name__}")
        print(traceback.format_exc())
        print()

# Ruta para servir el archivo HTML principal
@app.route('/')
def home():
    return send_file('app_citas_medicas.html')

@app.route('/enviar_cita', methods=['POST'])
def enviar_cita():
    try:
        data = request.json

        rut = data.get('rut')
        nombre = data.get('nombre')
        edad = data.get('edad')
        genero = data.get('genero')
        especialista = data.get('especialista')
        celular = data.get('celular')
        email_paciente = data.get('email')
        dia = data.get('dia')
        hora = data.get('hora')
        codigo_anulacion = data.get('codigo')

        # ✅ VALIDACIÓN: Verificar que NO exista otra cita activa en ese día y hora
        cita_existente = Reserva.query.filter_by(
            dia=dia,
            hora=hora,
            estado='activa'
        ).first()

        if cita_existente:
            return jsonify({
                'success': False,
                'message': f'❌ Lo siento, esa hora ya fue reservada. Por favor, elige otra hora.'
            }), 400

        # Guardar en base de datos
        nueva_reserva = Reserva(
            rut=rut,
            nombre=nombre,
            edad=edad,
            genero=genero,
            especialista=especialista,
            celular=celular,
            email=email_paciente,
            dia=dia,
            hora=hora,
            codigo_anulacion=codigo_anulacion,
            estado='activa'
        )
        db.session.add(nueva_reserva)
        db.session.commit()

        # Preparar cuerpo del email en TEXTO PLANO (sin HTML)
        cuerpo_html = f"""Hola {nombre},

Tu cita ha sido confirmada en nuestro sistema.

DATOS DE TU CITA:
Especialista: {especialista}
Fecha: {dia}
Hora: {hora}

DATOS PERSONALES REGISTRADOS:
Nombre: {nombre}
RUT: {rut}
Celular: +56{celular}
Email: {email_paciente}

IMPORTANTE - Código para anular: {codigo_anulacion}

Si necesitas cancelar o cambiar tu cita, usa el código anterior en nuestro sistema de citas.

Fecha de registro: {datetime.now().strftime('%d/%m/%Y %H:%M')}

Gracias por usar nuestro servicio de citas.

Consultas Psicologicas
Sistema de Reservas Online
"""

        # Crear versión en texto plano
        cuerpo_texto = f"""
        Confirmación de Cita Médica

        Detalles de tu cita:
        Nombre: {nombre}
        RUT: {rut}
        Edad: {edad}
        Género: {genero}
        Especialista: {especialista}
        Celular: +56{celular}
        Email: {email_paciente}
        Día: {dia}
        Hora: {hora}

        Código de Anulación: {codigo_anulacion}
        (Guarda este código si necesitas anular tu cita)

        Tu cita ha sido confirmada exitosamente.
        Por favor, no olvides asistir a tu consulta.

        Fecha de registro: {datetime.now().strftime('%d/%m/%Y %H:%M')}
        """

        # Enviar correos en background (sin bloquear la respuesta)
        # Email al paciente
        thread_paciente = threading.Thread(
            target=enviar_email_async,
            args=(email_paciente, f'Cita confirmada - {nombre}', cuerpo_html, cuerpo_texto)
        )
        thread_paciente.daemon = True
        thread_paciente.start()

        # Email al administrador
        cuerpo_admin = f"""
        Nueva cita agendada en el sistema:

        Nombre: {nombre}
        Email: {email_paciente}
        RUT: {rut}
        Edad: {edad}
        Género: {genero}
        Especialista: {especialista}
        Celular: +56{celular}
        Día: {dia}
        Hora: {hora}
        Código de Anulación: {codigo_anulacion}

        Fecha/Hora de registro: {datetime.now().strftime('%d/%m/%Y %H:%M')}
        """

        thread_admin = threading.Thread(
            target=enviar_email_async,
            args=(SENDER_EMAIL, f'Nueva Cita Agendada - {nombre}', f'<pre>{cuerpo_admin}</pre>', cuerpo_admin)
        )
        thread_admin.daemon = True
        thread_admin.start()

        return jsonify({'success': True, 'message': 'Cita agendada exitosamente. Se enviarán los correos de confirmación.'})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400

@app.route('/buscar_reserva', methods=['POST'])
def buscar_reserva():
    """Buscar reserva por código de anulación"""
    try:
        data = request.json
        codigo = data.get('codigo', '').strip().upper()

        # Buscar en base de datos
        reserva = Reserva.query.filter_by(codigo_anulacion=codigo, estado='activa').first()

        if not reserva:
            return jsonify({'success': False, 'message': 'Código de anulación inválido o cita ya fue anulada'}), 404

        return jsonify({'success': True, 'reserva': reserva.to_dict()})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400

@app.route('/anular_reserva', methods=['POST'])
def anular_reserva():
    """Anular una reserva por código"""
    try:
        data = request.json
        codigo = data.get('codigo', '').strip().upper()

        # Buscar y anular
        reserva = Reserva.query.filter_by(codigo_anulacion=codigo, estado='activa').first()

        if not reserva:
            return jsonify({'success': False, 'message': 'Código inválido o cita ya fue anulada'}), 404

        # Marcar como anulada
        reserva.estado = 'anulada'
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Cita del {reserva.dia} a las {reserva.hora} anulada exitosamente',
            'reserva': reserva.to_dict()
        })

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400

@app.route('/obtener_citas', methods=['GET'])
def obtener_citas():
    """Obtener todas las citas activas para llenar el calendario"""
    try:
        # Obtener todas las citas activas
        citas = Reserva.query.filter_by(estado='activa').all()

        # Convertir a formato que entienda el frontend
        citas_lista = []
        for cita in citas:
            citas_lista.append({
                'day': cita.dia,
                'time': cita.hora,
                'rut': cita.rut,
                'nombre': cita.nombre,
                'email': cita.email
            })

        return jsonify({
            'success': True,
            'citas': citas_lista,
            'cantidad': len(citas_lista)
        })

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("✅ Servidor configurado correctamente")
    print("=" * 60)
    print(f"\n📧 Email: {SENDER_EMAIL}")
    print("🔐 Contraseña: [Protegida en .env]")
    print(f"💾 Base de datos: {db_path}")
    print("\n* Running on http://localhost:5000")
    print("Press CTRL+C to quit\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
