
import uuid
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from python.models import db
from python.models.sistema import *

class Inventario(db.Model,BaseMixin,AuditMixin):
    
    id_sucursal = db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=False)
    id_producto = db.Column(db.UUID, db.ForeignKey("productos.id"), nullable=False)

    cantidad = db.Column(db.Numeric(15, 3), nullable=False, default=0)
    cantidad_en_transito = db.Column(db.Numeric(15, 3), nullable=False, default=0)

    sucursal = db.relationship("Sucursales", backref="inventario", lazy=True)
    producto = db.relationship("Productos", backref="inventario", lazy=True)

class AjustesDeInventario(db.Model,BaseMixin,AuditMixin):
    
    id_sucursal = db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=False)
    id_producto = db.Column(db.UUID, db.ForeignKey("productos.id"), nullable=False)

    fecha_de_ajuste = db.Column(db.Date)
    tipo_de_ajuste = db.Column(db.String(10),nullable=False, default="Entrada")
    cantidad = db.Column(db.Numeric(15, 3), nullable=False, default=0)
    notas = db.Column(db.Text)
    estatus = db.Column(db.String(50),nullable=False, default="En revisión")

    sucursal = db.relationship("Sucursales", backref="ajustes_de_inventario", lazy=True)
    producto = db.relationship("Productos", backref="ajustes_de_inventario", lazy=True)

    @validates('cantidad')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value


class TransferenciasDeInventario(db.Model,BaseMixin,AuditMixin):
    id_sucursal_salida = db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=False)
    id_sucursal_entrada = db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=False)

    fecha_de_transferencia= db.Column(db.Date)
    notas = db.Column(db.Text)
    estatus = db.Column(db.String(50),nullable=False, default="En revisión")

    sucursal_salida = db.relationship("Sucursales",foreign_keys=[id_sucursal_salida], backref="transferencias_de_inventario_salida", lazy="joined")
    sucursal_entrada = db.relationship("Sucursales",foreign_keys=[id_sucursal_entrada], backref="transferencias_de_inventario_entrada", lazy="joined")

class ProductosEnTransferenciasDeInventario(db.Model,BaseMixin,AuditMixin):
    id_transferencia_de_inventario = db.Column(db.UUID, db.ForeignKey("transferencias_de_inventario.id"), nullable=False)
    id_producto = db.Column(db.UUID, db.ForeignKey("productos.id"), nullable=False)

    cantidad = db.Column(db.Numeric(15, 3), nullable=False, default=0)

    transferencia_de_inventario = db.relationship("TransferenciasDeInventario", backref="productos_en_transferencias_de_inventario", lazy="joined")
    producto = db.relationship("Productos", backref="productos_en_transferencias_de_inventario", lazy="joined")

    @validates('cantidad')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value
