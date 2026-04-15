from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.database import get_db
from utils.crypto import hash_password, verify_password
import re

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/', methods=['GET', 'POST'])
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        usuario = request.form.get('usuario', '').strip()
        password = request.form.get('password', '').strip()

        if not usuario or not password:
            flash('Por favor diligencie todos los campos.', 'danger')
            return render_template('login.html')

        conn = get_db()
        user = conn.execute(
            'SELECT * FROM usuarios WHERE usuario = ? AND estado = "Activo"', (usuario,)
        ).fetchone()
        conn.close()

        if user and verify_password(password, user['password_hash'], user['salt']):
            session['user_id'] = user['id']
            session['usuario'] = user['usuario']
            session['nombre'] = user['nombre']
            session['rol'] = user['rol']
            return redirect(url_for('dashboard.index'))
        else:
            flash('Usuario o contraseña incorrecta.', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada exitosamente.', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        cedula = request.form.get('cedula', '').strip()
        correo = request.form.get('correo', '').strip()
        usuario = request.form.get('usuario', '').strip()
        rol = request.form.get('rol', '').strip()
        password = request.form.get('password', '').strip()

        # Validations
        if not all([nombre, cedula, correo, usuario, rol, password]):
            flash('Todos los campos son obligatorios.', 'danger')
            return render_template('register.html')

        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', nombre):
            flash('El nombre solo debe contener texto.', 'danger')
            return render_template('register.html')

        if not cedula.isdigit():
            flash('La cédula debe contener solo números.', 'danger')
            return render_template('register.html')

        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', correo):
            flash('El correo electrónico no tiene un formato válido.', 'danger')
            return render_template('register.html')

        if not re.match(r'^[A-Za-z0-9áéíóúÁÉÍÓÚñÑ]+$', usuario):
            flash('El usuario solo debe contener texto.', 'danger')
            return render_template('register.html')

        if rol not in ('Administrador', 'Auxiliar'):
            flash('Seleccione un rol válido.', 'danger')
            return render_template('register.html')

        # Hash password
        pwd_hash, salt = hash_password(password)

        conn = get_db()
        try:
            conn.execute('''
                INSERT INTO usuarios (nombre, cedula, correo, usuario, rol, password_hash, salt)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (nombre, cedula, correo, usuario, rol, pwd_hash, salt))
            conn.commit()
            flash('Usuario registrado exitosamente.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            error_msg = str(e)
            if 'UNIQUE' in error_msg:
                flash('El usuario ya se encuentra registrado.', 'danger')
            else:
                flash('Error al registrar el usuario.', 'danger')
        finally:
            conn.close()

    return render_template('register.html')


@auth_bp.route('/recover', methods=['GET', 'POST'])
def recover():
    if request.method == 'POST':
        correo = request.form.get('correo', '').strip()
        nueva_password = request.form.get('nueva_password', '').strip()

        if not correo or not nueva_password:
            flash('Todos los campos son obligatorios.', 'danger')
            return render_template('recover.html')

        conn = get_db()
        user = conn.execute('SELECT * FROM usuarios WHERE correo = ?', (correo,)).fetchone()

        if user:
            pwd_hash, salt = hash_password(nueva_password)
            conn.execute(
                'UPDATE usuarios SET password_hash = ?, salt = ? WHERE correo = ?',
                (pwd_hash, salt, correo)
            )
            conn.commit()
            conn.close()
            flash('Contraseña actualizada exitosamente. Por favor inicie sesión.', 'success')
            return redirect(url_for('auth.login'))
        else:
            conn.close()
            flash('No se encontró un usuario con ese correo.', 'danger')

    return render_template('recover.html')
