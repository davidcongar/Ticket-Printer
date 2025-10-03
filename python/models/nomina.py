import uuid
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from python.models import db
from python.models.sistema import *

class PagosDeNomina(db.Model,BaseMixin,AuditMixin):

    id_sucursal = db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=False)
    id_cuenta_de_banco = db.Column(db.UUID, db.ForeignKey("cuentas_de_banco.id"), nullable=False)

    fecha = db.Column(db.Date, nullable=True)
    importe_total = db.Column(db.Float, nullable=False, default=0.00)
    notas = db.Column(db.Text) 
    estatus = db.Column(db.String(50), default="En revisión")

    sucursal = db.relationship("Sucursales", backref="pagos_de_nomina", lazy=True)
    cuenta_de_banco = db.relationship("CuentasDeBanco", backref="pagos_de_nomina", lazy=True)


class SueldosPagadosEnNomina(db.Model,BaseMixin,AuditMixin):

    id_pago_de_nomina = db.Column(db.UUID, db.ForeignKey("pagos_de_nomina.id"), nullable=False)
    id_empleado = db.Column(db.UUID, db.ForeignKey("empleados.id"), nullable=False)
    importe = db.Column(db.Float, nullable=False)
    importe_ajuste = db.Column(db.Float, nullable=False, default=0.00)
    importe_total = db.Column(db.Float, nullable=False, default=0.00)
    notas = db.Column(db.Text) 

    pago_de_nomina = db.relationship("PagosDeNomina", backref="sueldos_pagados_en_nomina", lazy=True)
    empleado = db.relationship("Empleados", backref="sueldos_pagados_en_nomina", lazy=True)

    @validates('importe')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value

class SueldosDeEmpleados(db.Model,BaseMixin,AuditMixin):

    id_sucursal = db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=False) 
    id_empleado = db.Column(db.UUID, db.ForeignKey("empleados.id"), nullable=False)
    
    sueldo = db.Column(db.Float, nullable=False)
    estatus = db.Column(db.String(50), default="Activo")

    sucursal = db.relationship("Sucursales", backref="sueldos_de_empleados", lazy=True)
    empleado = db.relationship("Empleados", backref="sueldos_de_empleados", lazy=True)

    @validates('sueldo')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value
