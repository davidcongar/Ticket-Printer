import uuid
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from python.models import db
from sqlalchemy.orm import validates
from decimal import Decimal
from sqlalchemy.types import TypeDecorator, String
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv 

load_dotenv()

# Load your key securely (from env, Parameter Store, or Secrets Manager)
FERNET_KEY = os.environ["ENCRYPTION_KEY"]
fernet = Fernet(FERNET_KEY)

class BaseMixin:
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_visualizacion = db.Column(db.Integer)
    fecha_de_creacion = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp())
    fecha_de_actualizacion = db.Column(db.DateTime, onupdate=db.func.now())

class AuditMixin:
    id_usuario = db.Column(db.UUID, nullable=True)
    id_empresa = db.Column(db.UUID, nullable=True)

class EncryptedColumn(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        """Called before saving to the DB"""
        if value is None:
            return value
        if not isinstance(value, str):
            value = str(value)
        return fernet.encrypt(value.encode()).decode()

    def process_result_value(self, value, dialect):
        """Called after reading from the DB"""
        if value is None:
            return value
        try:
            return fernet.decrypt(value.encode()).decode()
        except Exception:
            # Handle old unencrypted values gracefully
            return value

class Empresas(db.Model,BaseMixin):
    __tablename__ = "empresas"
    
    nombre_empresa = db.Column(db.String(255), nullable=False)
    nombre_contacto = db.Column(db.String(255), nullable=True)
    telefono_contacto = db.Column(db.String(255), nullable=True)
    correo_electronico_contacto = db.Column(db.String(120), unique=True, nullable=True)
    paquete_contratado = db.Column(db.String(120), nullable=True)
    is_pedidos_en_linea = db.Column(db.Boolean, nullable=True)
    is_pedidos_en_linea_telefono = db.Column(db.Boolean, nullable=True)
    is_ordenes_cocina = db.Column(db.Boolean, nullable=True)
    estatus = db.Column(db.String(255),default="Activo")

class Usuarios(db.Model,BaseMixin):
    __tablename__ = "usuarios"
    
    id_empresa = db.Column(db.UUID, db.ForeignKey("empresas.id"))
    id_rol = db.Column(db.UUID, db.ForeignKey("roles.id"))
    id_sucursal = db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=True)
    nombre = db.Column(db.String(1000), nullable=False)
    correo_electronico = db.Column(db.String(120), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    contrasena_api = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4)
    intentos_de_inicio_de_sesion = db.Column(db.Integer, default=0)
    ultima_sesion=db.Column(db.DateTime, nullable=True)
    ultimo_cambio_de_contrasena=db.Column(db.Date, nullable=True)
    codigo_unico = db.Column(db.UUID)
    codigo_unico_expira = db.Column(db.DateTime)
    estatus = db.Column(db.String(255),default="Activo")
    
    empresa = db.relationship("Empresas", backref="usuarios", lazy=True)
    sucursal = db.relationship("Sucursales", backref="usuarios", lazy=True)
    rol = db.relationship("Roles", backref="usuarios", lazy=True)

    # Métodos
    def set_password(self, password):
        self.contrasena = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.contrasena, password)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"<usuarios(id={self.id}, nombre={self.nombre}, correo={self.correo_electronico})>"

class LogsAuditoria(db.Model):
    __tablename__ = "logs_auditoria"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tabla = db.Column(db.String(255), nullable=False)
    id_registro = db.Column(db.String(255), nullable=False)
    usuario = db.Column(db.String(255), nullable=True, server_default="Desconocido")
    empresa = db.Column(db.String(255), nullable=True, server_default="Desconocido")
    accion = db.Column(db.String(1000), nullable=False)
    datos_anteriores = db.Column(db.Text, nullable=True)
    datos_nuevos = db.Column(db.Text, nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return (
            f"<LogsAuditoria {self.accion} en {self.tabla} registro {self.id_registro}>"
        )

class CategoriasDeReportes(db.Model,BaseMixin,AuditMixin):
    nombre = db.Column(db.String(50), nullable=False)
    estatus = db.Column(db.String(255),default="Activo")

class Reportes(db.Model,BaseMixin,AuditMixin):
    nombre = db.Column(db.String(50), nullable=False)
    id_categoria_de_reporte = db.Column(db.UUID,db.ForeignKey('categorias_de_reportes.id'),nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    ruta_sql = db.Column(db.String(255), nullable=False)
    estatus = db.Column(db.String(255),default="Activo")

    categoria = db.relationship("CategoriasDeReportes", backref="reportes", lazy=True)

relacion_rutas_roles = db.Table(
    "relacion_rutas_roles",
    db.Column(
        "id_ruta",
        db.UUID,
        db.ForeignKey("rutas.id"),
        primary_key=True,
    ),
    db.Column(
        "id_rol",
        db.UUID,
        db.ForeignKey("roles.id"),
        primary_key=True,
    ),
)

class Roles(db.Model,BaseMixin,AuditMixin):
    __tablename__ = "roles"

    nombre = db.Column(db.String(1000))
    estatus = db.Column(db.String(255),default="Activo")

class Rutas(db.Model,BaseMixin,AuditMixin):
    __tablename__ = "rutas"
    categoria = db.Column(db.String(255))
    nombre = db.Column(db.String(255))
    ruta = db.Column(db.String(255))
    roles = db.relationship(
        "Roles",
        secondary=relacion_rutas_roles,
        backref=db.backref("rutas", lazy="dynamic")  # ← este es el cambio
    )

class Archivos(db.Model,AuditMixin):
    id = db.Column(db.UUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre_del_archivo =db.Column(db.String(255))
    tabla_origen=db.Column(db.String(255), nullable=False)
    id_registro=db.Column(db.UUID, nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    ruta_s3 = db.Column(db.String(255), nullable=False)
    fecha_de_creacion = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __repr__(self):
        return (
            f"<Archivo (id={self.id}, nombre={self.nombre}, ruta={self.ruta_s3})>"
        )
    
    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}