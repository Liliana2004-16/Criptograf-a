from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.database import get_db

ventas_bp = Blueprint('ventas', __name__)

PRODUCTOS = [
    'Kefir Plur Botella 1000g',
    'Yogo yogo Bolsa 900g',
    'Yogurt Original Bolsa 900g',
    'Avena Vaso 250g',
    'Yox Botella 100g'
]


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@ventas_bp.route('/ventas')
@login_required
def list_ventas():
    conn = get_db()
    ventas = conn.execute('''
        SELECT v.*, u.nombre as nombre_usuario
        FROM ventas v
        JOIN usuarios u ON v.usuario_id = u.id
        ORDER BY v.fecha DESC
    ''').fetchall()
    conn.close()
    return render_template('ventas.html', ventas=ventas)


@ventas_bp.route('/ventas/registrar', methods=['GET', 'POST'])
@login_required
def registrar_venta():
    conn = get_db()

    # Get next consecutivo
    result = conn.execute('SELECT MAX(consecutivo) as max_cons FROM ventas').fetchone()
    next_cons = (result['max_cons'] or 0) + 1

    if request.method == 'POST':
        cliente = request.form.get('cliente', '').strip()
        nit_cc = request.form.get('nit_cc', '').strip()
        producto = request.form.get('producto', '').strip()
        valor_str = request.form.get('valor', '').strip()

        if not all([cliente, nit_cc, producto, valor_str]):
            flash('Todos los campos son obligatorios.', 'danger')
            conn.close()
            return render_template('registrar_venta.html', consecutivo=next_cons, productos=PRODUCTOS)

        if not nit_cc.isdigit():
            flash('El NIT/CC debe contener solo números.', 'danger')
            conn.close()
            return render_template('registrar_venta.html', consecutivo=next_cons, productos=PRODUCTOS)

        if producto not in PRODUCTOS:
            flash('Producto inválido.', 'danger')
            conn.close()
            return render_template('registrar_venta.html', consecutivo=next_cons, productos=PRODUCTOS)

        try:
            valor = float(valor_str.replace(',', '').replace('.', ''))
        except ValueError:
            flash('El valor debe ser un número válido.', 'danger')
            conn.close()
            return render_template('registrar_venta.html', consecutivo=next_cons, productos=PRODUCTOS)

        try:
            conn.execute('''
                INSERT INTO ventas (consecutivo, cliente, nit_cc, producto, valor, usuario_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (next_cons, cliente, nit_cc, producto, valor, session['user_id']))
            conn.commit()
            flash('Venta registrada exitosamente.', 'success')
            return redirect(url_for('ventas.list_ventas'))
        except Exception:
            flash('Error al registrar la venta.', 'danger')
        finally:
            conn.close()
    else:
        conn.close()

    return render_template('registrar_venta.html', consecutivo=next_cons, productos=PRODUCTOS)
