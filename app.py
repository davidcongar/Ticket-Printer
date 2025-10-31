# app.py

import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, flash, g, redirect, session, url_for
from flask_migrate import Migrate
from sqlalchemy import event, inspect

from flask_session import Session
from python.models.modelos import db



# Cargar variables de entornoa
load_dotenv()

# Inicializar la Aplicación
app = Flask(__name__)

# Configuración de la Aplicación
app.secret_key = os.urandom(24)
app.config["SESSION_TYPE"] = "filesystem"
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Configuración de la sesión
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(weeks=1)
Session(app)


@app.before_request
def make_session_permanent():
    """Hacer que la sesión sea permanente y respetar el tiempo de expiración."""
    session.permanent = True


# Configuración de Base de Datos
app.config.update(
    SQLALCHEMY_DATABASE_URI=(
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    ),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_ENGINE_OPTIONS={
        "pool_size": 5,
        "pool_recycle": 280,
        "pool_pre_ping": True,
        "pool_timeout": 30,
        "max_overflow": 10,
    },
)

from sqlalchemy import event
from sqlalchemy.exc import DisconnectionError

@event.listens_for(db.engine, "engine_connect")
def ping_connection(connection, branch):
    if branch:
        return
    try:
        connection.scalar("SELECT 1")
    except DisconnectionError:
        connection.invalidate()
        connection.scalar("SELECT 1")

# Inicializar extensiones
db.init_app(app)
migrate = Migrate(app, db)
Session(app)

from python.routes.ordenes_de_venta import ordenes_de_venta_bp
app.register_blueprint(ordenes_de_venta_bp)


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=False)
