from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv

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

# Configuración de correo desde variables de entorno (SEGURO - NO SE EXPONE EN GITHUB)
SENDER_EMAIL = os.getenv('GMAIL_EMAIL')
SENDER_PASSWORD = os.getenv('GMAIL_PASSWORD')

# Validar que las variables estén configuradas
if not SENDER_EMAIL or not SENDER_PASSWORD:
    print("\n" + "=" * 60)
    print("❌ ERROR: Falta configuración")
    print("=" * 60)
    print("\nDebes crear un archivo .env con:\n")
    print("GMAIL_EMAIL=tu_email@gmail.com")
    print("GMAIL_PASSWORD=xxxx xxxx xxxx xxxx")
    print("\n" + "=" * 60 + "\n")
    raise ValueError("Las variables GMAIL_EMAIL y GMAIL_PASSWORD no están configuradas")

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

        # Crear mensaje de correo
        mensaje = MIMEMultipart('alternative')
        mensaje['Subject'] = 'Confirmación de Cita Médica - Consultas Psicológicas'
        mensaje['From'] = SENDER_EMAIL
        mensaje['To'] = email_paciente

        # Crear cuerpo en HTML
        cuerpo_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="max-width: 500px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h2 style="color: #66bb6a; text-align: center;">✓ Cita Agendada Exitosamente</h2>

                    <hr style="border: none; border-top: 2px solid #66bb6a; margin: 20px 0;">

                    <h3 style="color: #1a237e;">Detalles de tu cita:</h3>

                    <table style="width: 100%; border-collapse: collapse;">
                        <tr style="background-color: #f0f7ee;">
                            <td style="padding: 10px; font-weight: bold; color: #1a237e;">Nombre:</td>
                            <td style="padding: 10px;">{nombre}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; font-weight: bold; color: #1a237e;">RUT:</td>
                            <td style="padding: 10px;">{rut}</td>
                        </tr>
                        <tr style="background-color: #f0f7ee;">
                            <td style="padding: 10px; font-weight: bold; color: #1a237e;">Edad:</td>
                            <td style="padding: 10px;">{edad}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; font-weight: bold; color: #1a237e;">Género:</td>
                            <td style="padding: 10px;">{genero}</td>
                        </tr>
                        <tr style="background-color: #f0f7ee;">
                            <td style="padding: 10px; font-weight: bold; color: #1a237e;">Especialista:</td>
                            <td style="padding: 10px;">{especialista}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; font-weight: bold; color: #1a237e;">Celular:</td>
                            <td style="padding: 10px;">+56{celular}</td>
                        </tr>
                        <tr style="background-color: #f0f7ee;">
                            <td style="padding: 10px; font-weight: bold; color: #1a237e;">Email:</td>
                            <td style="padding: 10px;">{email_paciente}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; font-weight: bold; color: #1a237e;">Día:</td>
                            <td style="padding: 10px;">{dia}</td>
                        </tr>
                        <tr style="background-color: #f0f7ee;">
                            <td style="padding: 10px; font-weight: bold; color: #1a237e;">Hora:</td>
                            <td style="padding: 10px;">{hora}</td>
                        </tr>
                    </table>

                    <hr style="border: none; border-top: 2px solid #66bb6a; margin: 20px 0;">

                    <p style="color: #666; font-size: 14px;">
                        <strong>Fecha de registro:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}
                    </p>

                    <div style="background-color: #e3f2fd; border-left: 4px solid #2196F3; padding: 15px; margin: 20px 0; border-radius: 4px;">
                        <p style="color: #0d47a1; margin: 0; font-size: 13px;">
                            <strong>🔐 Código de Anulación:</strong><br>
                            <span style="font-family: monospace; font-weight: bold; font-size: 16px; color: #1565c0;">{codigo_anulacion}</span><br>
                            <span style="font-size: 12px; color: #1976d2;">Guarda este código si necesitas anular tu cita más adelante</span>
                        </p>
                    </div>

                    <div style="background-color: #c8e6c9; border-left: 4px solid #66bb6a; padding: 15px; margin: 20px 0; border-radius: 4px;">
                        <p style="color: #1b5e20; margin: 0;">
                            Tu cita ha sido confirmada exitosamente. Por favor, no olvides asistir a tu consulta.
                        </p>
                    </div>

                    <p style="color: #999; font-size: 12px; text-align: center; margin-top: 20px;">
                        Este es un correo automático. Por favor, no respondas a este mensaje.
                    </p>
                </div>
            </body>
        </html>
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

        # Adjuntar ambas versiones
        parte_texto = MIMEText(cuerpo_texto, 'plain')
        parte_html = MIMEText(cuerpo_html, 'html')

        mensaje.attach(parte_texto)
        mensaje.attach(parte_html)

        # Enviar correo al paciente
        try:
            servidor = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            servidor.login(SENDER_EMAIL, SENDER_PASSWORD)
            servidor.sendmail(SENDER_EMAIL, email_paciente, mensaje.as_string())
            servidor.quit()

            # Enviar copia al administrador
            mensaje_admin = MIMEMultipart('alternative')
            mensaje_admin['Subject'] = f'Nueva Cita Agendada - {nombre}'
            mensaje_admin['From'] = SENDER_EMAIL
            mensaje_admin['To'] = SENDER_EMAIL

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

            parte_admin = MIMEText(cuerpo_admin, 'plain')
            mensaje_admin.attach(parte_admin)

            servidor = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            servidor.login(SENDER_EMAIL, SENDER_PASSWORD)
            servidor.sendmail(SENDER_EMAIL, SENDER_EMAIL, mensaje_admin.as_string())
            servidor.quit()

            return jsonify({'success': True, 'message': 'Correo enviado exitosamente'})

        except smtplib.SMTPAuthenticationError:
            return jsonify({'success': False, 'message': 'Error de autenticación. Verifica la contraseña de aplicación de Gmail.'}), 401
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error al enviar correo: {str(e)}'}), 500

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
