from flask import Flask
from models.database import init_db
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.users import users_bp
from routes.ventas import ventas_bp
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(users_bp)
app.register_blueprint(ventas_bp)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
