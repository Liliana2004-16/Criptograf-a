from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models.database import get_db

users_bp = Blueprint('users', __name__)


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@users_bp.route('/usuarios')
@login_required
def list_users():
    if session.get('rol') != 'Administrador':
        flash('Usted No esta Autorizado.', 'danger')
        return redirect(url_for('dashboard.index'))

    conn = get_db()
    users = conn.execute('SELECT id, nombre, cedula, usuario, correo, rol, estado FROM usuarios').fetchall()
    conn.close()
    return render_template('usuarios.html', users=users)


@users_bp.route('/usuarios/estado', methods=['POST'])
@login_required
def update_estado():
    if session.get('rol') != 'Administrador':
        return jsonify({'error': 'No autorizado'}), 403

    user_id = request.form.get('user_id')
    estado = request.form.get('estado')

    if estado not in ('Activo', 'Inactivo'):
        flash('Estado inválido.', 'danger')
        return redirect(url_for('users.list_users'))

    conn = get_db()
    conn.execute('UPDATE usuarios SET estado = ? WHERE id = ?', (estado, user_id))
    conn.commit()
    conn.close()
    flash('Estado del usuario actualizado.', 'success')
    return redirect(url_for('users.list_users'))
