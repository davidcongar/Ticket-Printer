import uuid
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from python.models import db
from python.models.sistema import *


class OrdenesDeCompra(db.Model,BaseMixin,AuditMixin):

    id_sucursal = db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=False) 
    id_proveedor = db.Column(db.UUID, db.ForeignKey("proveedores.id"), nullable=False)

    fecha_orden = db.Column(db.Date, nullable=False)
    fecha_entrega_estimada = db.Column(db.Date) 
    fecha_entrega_real = db.Column(db.Date)  

    subtotal = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    costo_de_envio = db.Column(db.Numeric(15, 2), nullable=True, default=0.00)
    otros_costos = db.Column(db.Numeric(15, 2), nullable=True, default=0.00)
    descuentos = db.Column(db.Numeric(15, 2), default=0.00)
    importe_total = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    importe_pagado = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    notas = db.Column(db.Text)

    estatus = db.Column(db.String(255),default="En revisión") # e.g., En revisión, Aprobada, Recibida,Cancelada
    estatus_de_pago = db.Column(db.String(255),default="Sin pagar") # e.g., Sin pagar, Pagada, Pagada parcial

    proveedor = db.relationship("Proveedores", backref="ordenes_de_compra", lazy=True)
    sucursal = db.relationship("Sucursales", backref="ordenes_de_compra", lazy=True)

class ProductosEnOrdenesDeCompra(db.Model,BaseMixin,AuditMixin):

    id_orden_de_compra = db.Column(db.UUID, db.ForeignKey("ordenes_de_compra.id"), nullable=False) 
    id_producto = db.Column(db.UUID, db.ForeignKey("productos.id"), nullable=False) 

    cantidad_ordenada = db.Column(db.Numeric(15, 3), nullable=False, default=0)
    cantidad_recibida = db.Column(db.Numeric(15, 3), default=0)
    precio_unitario = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    subtotal = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    descuento_porcentaje = db.Column(db.Numeric(15, 2), default=0.00)
    importe_total= db.Column(db.Numeric(15, 2), default=0.00)
    fecha_entrega_estimada = db.Column(db.Date) 
    notas = db.Column(db.Text) 
    estatus = db.Column(db.String(255),default="Pendiente") # e.g., Pendiente, Recibido,Cancelado

    orden_de_compra = db.relationship("OrdenesDeCompra", backref="productos_en_ordenes_de_compra", lazy=True)
    producto = db.relationship("Productos", backref="productos_en_ordenes_de_compra", lazy=True)

    @validates('cantidad_ordenada', 'cantidad_recibida', 'precio_unitario', 'subtotal', 'descuento_porcentaje', 'importe_total')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value

class EntregaDeProductosEnOrdenesDeCompra(db.Model,BaseMixin,AuditMixin):

    id_producto_en_orden_de_compra = db.Column(db.UUID, db.ForeignKey("productos_en_ordenes_de_compra.id"), nullable=False) 

    cantidad_recibida = db.Column(db.Numeric(15, 3), nullable=False, default=0)
    fecha_entrega = db.Column(db.Date) 

    producto_en_orden_de_compra = db.relationship("ProductosEnOrdenesDeCompra", backref="entrega_de_productos_en_ordenes_de_compra", lazy=True)

    @validates('cantidad_recibida')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value

class Gastos(db.Model,BaseMixin,AuditMixin):

    id_sucursal = db.Column(db.UUID, db.ForeignKey("sucursales.id"),nullable=False)
    id_categoria_de_gasto=db.Column(db.UUID, db.ForeignKey("categorias_de_gastos.id"),nullable=False)
    id_proveedor = db.Column(db.UUID, db.ForeignKey("proveedores.id"),nullable=False)

    importe =db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    importe_pagado = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    fecha_de_gasto = db.Column(db.Date)
    notas = db.Column(db.Text)
    estatus = db.Column(db.String(100),nullable=False, default="En revisión") # en revision,aprobado, pagado parcial, pagado

    proveedor = db.relationship('Proveedores', backref='gastos', lazy='joined')
    categoria = db.relationship('CategoriasDeGastos', backref='gastos', lazy='joined')
    sucursal = db.relationship('Sucursales', backref='gastos', lazy='joined')

    @validates('importe')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value


class Pagos(db.Model,BaseMixin,AuditMixin):

    id_sucursal = db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=False) 
    id_proveedor = db.Column(db.UUID, db.ForeignKey("proveedores.id"), nullable=False) 
    id_cuenta_de_banco = db.Column(db.UUID, db.ForeignKey("cuentas_de_banco.id"), nullable=False) 

    fecha_pago = db.Column(db.Date, nullable=False)
    importe = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    notas = db.Column(db.Text)

    estatus = db.Column(db.String(255),default="En revisión") # e.g., En revisión, Aprobado, Pagado,Cancelado

    sucursal = db.relationship('Sucursales', backref='pagos', lazy='joined')
    proveedor = db.relationship("Proveedores", backref="pagos", lazy=True)
    cuenta_de_banco = db.relationship("CuentasDeBanco", backref="pagos", lazy=True)

class GastosYComprasEnPagos(db.Model,BaseMixin,AuditMixin):

    id_pago = db.Column(db.UUID, db.ForeignKey("pagos.id"), nullable=False) 
    id_orden_de_compra = db.Column(db.UUID, db.ForeignKey("ordenes_de_compra.id"), nullable=True) 
    id_gasto = db.Column(db.UUID, db.ForeignKey("gastos.id"), nullable=True) 

    importe = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    notas = db.Column(db.Text)

    pago = db.relationship("Pagos", backref="gastos_y_compras_en_pagos", lazy=True)
    orden_de_compra = db.relationship("OrdenesDeCompra", backref="gastos_y_compras_en_pagos", lazy=True)
    gasto = db.relationship("Gastos", backref="gastos_y_compras_en_pagos", lazy=True)

    @validates('importe')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value


class TransferenciasDeDinero(db.Model,BaseMixin,AuditMixin):

    id_sucursal = db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=False) 
    id_cuenta_de_banco_salida = db.Column(db.UUID, db.ForeignKey("cuentas_de_banco.id"), nullable=False)
    id_cuenta_de_banco_entrada = db.Column(db.UUID, db.ForeignKey("cuentas_de_banco.id"), nullable=False)

    fecha_de_transferencia= db.Column(db.Date)
    importe = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    notas = db.Column(db.Text)
    estatus = db.Column(db.String(50),nullable=False, default="En revisión")

    sucursal = db.relationship('Sucursales', backref='transferencias_de_dinero', lazy='joined')
    cuenta_de_banco_salida = db.relationship("CuentasDeBanco",foreign_keys=[id_cuenta_de_banco_salida], backref="transferencias_de_dinero_salida", lazy="joined")
    cuenta_de_banco_entrada = db.relationship("CuentasDeBanco",foreign_keys=[id_cuenta_de_banco_entrada], backref="transferencias_de_dinero_entrada", lazy="joined")

    @validates('importe')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value


class AjustesDeDinero(db.Model,BaseMixin,AuditMixin):
    
    id_sucursal = db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=False) 
    id_cuenta_de_banco = db.Column(db.UUID, db.ForeignKey("cuentas_de_banco.id"), nullable=False)

    fecha_de_ajuste = db.Column(db.Date)
    tipo_de_ajuste = db.Column(db.String(10),nullable=False, default="Entrada")
    importe = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    notas = db.Column(db.Text)
    estatus = db.Column(db.String(50),nullable=False, default="En revisión")

    sucursal = db.relationship('Sucursales', backref='ajustes_de_dinero', lazy='joined')
    cuenta_de_banco = db.relationship("CuentasDeBanco", backref="ajustes_de_dinero", lazy=True)

    @validates('importe')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value

