import uuid
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from python.models import db
from python.models.sistema import *

class CategoriasDeSucursales(db.Model,BaseMixin,AuditMixin):
    nombre = db.Column(db.String(255), nullable=False)
    estatus = db.Column(db.String(255),default="Activo")

class Sucursales(db.Model,BaseMixin,AuditMixin):

    id_categoria_de_sucursal = db.Column(db.UUID, db.ForeignKey("categorias_de_sucursales.id"), nullable=False)
    
    nombre = db.Column(db.String(255), nullable=False)
    direccion = db.Column(db.String(255), nullable=True)
    codigo_postal = db.Column(db.String(20))
    pais = db.Column(db.String(100))
    telefono = db.Column(db.String(50))
    correo_electronico = db.Column(db.String(255))
    fecha_apertura = db.Column(db.Date)
    horario_apertura = db.Column(db.Time, nullable=True)
    horario_cierre = db.Column(db.Time, nullable=True)
    estatus = db.Column(db.String(255),default="Activo")
    pedidos_online = db.Column(db.Boolean) 
    
    categoria = db.relationship("CategoriasDeSucursales", backref="sucursales", lazy=True)

class TurnosDeOperacion(db.Model,BaseMixin,AuditMixin):
    id_sucursal=db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=True)

    fecha_hora_apertura = db.Column(db.DateTime, nullable=True)
    fecha_hora_cierre=db.Column(db.DateTime, nullable=True)
    estatus = db.Column(db.String(255),default="En proceso")

    sucursal = db.relationship("Sucursales", backref="turnos_de_operacion", lazy=True)

class Puestos(db.Model,BaseMixin,AuditMixin):
    nombre = db.Column(db.String(255), nullable=False)
    descripcion=db.Column(db.String(500), nullable=True)
    estatus = db.Column(db.String(255),default="Activo")

class Empleados(db.Model,BaseMixin,AuditMixin):

    id_sucursal=db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=True)
    id_puesto=db.Column(db.UUID, db.ForeignKey("puestos.id"), nullable=False)

    nombre_completo = db.Column(db.String(255), nullable=False)
    fecha_nacimiento = db.Column(db.Date)
    genero = db.Column(db.String(20))
    estado_civil = db.Column(db.String(50))
    direccion = db.Column(db.String(255))
    codigo_postal = db.Column(db.String(20))
    telefono = db.Column(db.String(50))
    correo_electronico = db.Column(db.String(255))
    fecha_contratacion = db.Column(db.Date, nullable=False)
    fecha_terminacion = db.Column(db.Date)
    numero_seguridad_social = db.Column(db.String(50))
    rfc = db.Column(db.String(20))
    curp = db.Column(db.String(20))
    codigo_pos=db.Column(db.Integer)
    estatus = db.Column(db.String(255),default="Activo")

    puesto = db.relationship("Puestos", backref="empleados", lazy=True)
    sucursal = db.relationship("Sucursales", backref="empleados", lazy=True)

class CategoriasDeProductos(db.Model,BaseMixin,AuditMixin):
    nombre = db.Column(db.String(255), nullable=False)
    descripcion=db.Column(db.String(500), nullable=True)
    estatus = db.Column(db.String(255),default="Activo")

class Productos(db.Model,BaseMixin,AuditMixin):

    id_sucursal = db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=False) 
    id_categoria_de_producto = db.Column(db.UUID, db.ForeignKey("categorias_de_productos.id"), nullable=False)

    nombre = db.Column(db.String(255), nullable=False)
    unidad_de_medida = db.Column(db.String(50))
    inventariable = db.Column(db.String(50)) 
    codigo_de_barras = db.Column(db.String(255), nullable=True)
    descripcion = db.Column(db.String(500), nullable=True)
    estatus = db.Column(db.String(255),default="Activo")

    sucursal = db.relationship('Sucursales', backref='productos', lazy='joined')
    categoria = db.relationship("CategoriasDeProductos", backref="productos", lazy=True)

class CategoriasDeMenu(db.Model,BaseMixin,AuditMixin):
    nombre = db.Column(db.String(255), nullable=False)
    descripcion=db.Column(db.String(500), nullable=True)
    estatus = db.Column(db.String(255),default="Activo")

class Menu(db.Model,BaseMixin,AuditMixin):

    id_sucursal = db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=False) 
    id_categoria_de_menu = db.Column(db.UUID, db.ForeignKey("categorias_de_menu.id"), nullable=True)

    nombre = db.Column(db.String(255), nullable=False)
    unidad_de_medida = db.Column(db.String(50)) 
    descripcion = db.Column(db.String(500), nullable=True)
    image_url = db.Column(db.String(50), nullable=True)
    estatus = db.Column(db.String(255),default="Activo")

    sucursal = db.relationship('Sucursales', backref='menu', lazy='joined')
    categoria = db.relationship("CategoriasDeMenu", backref="menu", lazy=True)

class Recetas(db.Model,BaseMixin,AuditMixin):

    id_menu = db.Column(db.UUID, db.ForeignKey("menu.id"), nullable=False) # producto principal
    id_producto = db.Column(db.UUID, db.ForeignKey("productos.id"), nullable=False) # producto utilizado en la receta

    cantidad = db.Column(db.Numeric(15, 3), nullable=False, default=0)
    
    menu = db.relationship("Menu", backref="recetas", lazy=True)
    producto = db.relationship("Productos", backref="recetas", lazy=True)

class ModificacionesDeMenu(db.Model,BaseMixin,AuditMixin):

    id_menu = db.Column(db.UUID, db.ForeignKey("menu.id"), nullable=True)

    nombre = db.Column(db.String(255), nullable=False)
    estatus = db.Column(db.String(255),default="Activo")

    menu = db.relationship("Menu", backref="modificaciones_de_menu", lazy=True)

class ComplementosDeMenu(db.Model,BaseMixin,AuditMixin):

    id_menu = db.Column(db.UUID, db.ForeignKey("menu.id"), nullable=True)

    nombre = db.Column(db.String(255), nullable=False)
    estatus = db.Column(db.String(255),default="Activo")

    menu = db.relationship("Menu", backref="complementos_de_menu", lazy=True)

class PreciosDeComplementosDeMenu(db.Model,BaseMixin,AuditMixin):

    id_sucursal = db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=False)
    id_canal_de_venta = db.Column(db.UUID, db.ForeignKey("canales_de_venta.id"), nullable=False)
    id_menu = db.Column(db.UUID, db.ForeignKey("menu.id"), nullable=False)
    id_complemento_de_menu = db.Column(db.UUID, db.ForeignKey("complementos_de_menu.id"), nullable=False)

    precio_unitario = db.Column(db.Float, nullable=False)
    estatus = db.Column(db.String(255),default="Activo")

    sucursal = db.relationship("Sucursales", backref="precios_de_complementos_de_menu", lazy=True)
    menu = db.relationship("Menu", backref="precios_de_complementos_de_menu", lazy=True)
    complemento_de_menu = db.relationship("ComplementosDeMenu", backref="precios_de_complementos_de_menu", lazy=True)
    canal_de_venta = db.relationship("CanalesDeVenta", backref="precios_de_complementos_de_menu", lazy=True)

    @validates('precio_unitario')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value

class RecetasDeComplementosDeMenu(db.Model,BaseMixin,AuditMixin):

    id_complemento_de_menu = db.Column(db.UUID, db.ForeignKey("complementos_de_menu.id"), nullable=False)
    id_producto = db.Column(db.UUID, db.ForeignKey("productos.id"), nullable=False)

    cantidad = db.Column(db.Numeric(15, 3), nullable=False, default=0)
    
    complemento_de_menu = db.relationship("ComplementosDeMenu", backref="recetas_de_complementos_de_menu", lazy=True)
    producto = db.relationship("Productos", backref="recetas_de_complementos_de_menu", lazy=True)

class Clientes(db.Model,BaseMixin,AuditMixin):

    id_sucursal=db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=True)

    nombre = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(50))
    correo_electronico = db.Column(db.String(255))
    direccion = db.Column(db.String(255))
    numero_exterior = db.Column(db.String(255))
    numero_interior = db.Column(db.String(255))
    instrucciones_de_entrega = db.Column(db.String(255))
    estatus = db.Column(db.String(255),default="Activo")

    sucursal = db.relationship("Sucursales", backref="clientes", lazy=True)


class Proveedores(db.Model,BaseMixin,AuditMixin):
    nombre = db.Column(db.String(255), nullable=False)
    razon_social = db.Column(db.String(255))
    rfc = db.Column(db.String(20))
    direccion = db.Column(db.String(255))
    codigo_postal = db.Column(db.String(20))
    telefono = db.Column(db.String(50))
    correo_electronico = db.Column(db.String(255))

    persona_contacto = db.Column(db.String(255))
    telefono_contacto = db.Column(db.String(50))
    correo_electronico_contacto = db.Column(db.String(255))
    condiciones_pago = db.Column(db.String(100)) 

    sitio_web = db.Column(db.String(255))
    estatus = db.Column(db.String(255),default="Activo")

class PreciosDeMenu(db.Model,BaseMixin,AuditMixin):

    id_sucursal = db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=False)
    id_canal_de_venta = db.Column(db.UUID, db.ForeignKey("canales_de_venta.id"), nullable=False)
    id_menu = db.Column(db.UUID, db.ForeignKey("menu.id"), nullable=False)

    precio_unitario = db.Column(db.Float, nullable=False)
    estatus = db.Column(db.String(255),default="Activo")

    sucursal = db.relationship("Sucursales", backref="precios_de_menu", lazy=True)
    menu = db.relationship("Menu", backref="precios_de_menu", lazy=True)
    canal_de_venta = db.relationship("CanalesDeVenta", backref="precios_de_menu", lazy=True)

    @validates('precio_unitario')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value


class CuentasDeBanco(db.Model,BaseMixin,AuditMixin):

    id_sucursal = db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=False) 
    banco = db.Column(db.String(100),nullable=False)
    tipo_de_cuenta = db.Column(db.String(100),nullable=False)
    nombre = db.Column(db.String(100),nullable=False)
    numero_de_cuenta = db.Column(db.String(100),nullable=False)
    clabe = db.Column(db.String(100),nullable=False)
    balance = db.Column(db.Numeric(15, 3), nullable=False, default=0)
    estatus = db.Column(db.String(255),default="Activo")

    sucursal = db.relationship("Sucursales", backref="cuentas_de_banco", lazy=True)

class CategoriasDeGastos(db.Model,BaseMixin,AuditMixin):
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(500))
    estatus = db.Column(db.String(255),default="Activo")

class CanalesDeVenta(db.Model,BaseMixin,AuditMixin):

    id_sucursal = db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=False) 
    id_cuenta_de_banco_efectivo = db.Column(db.UUID, db.ForeignKey("cuentas_de_banco.id"), nullable=True)
    id_cuenta_de_banco_terminal = db.Column(db.UUID, db.ForeignKey("cuentas_de_banco.id"), nullable=True)
    nombre = db.Column(db.String(255))
    estatus = db.Column(db.String(255),default="Activo")

    sucursal = db.relationship("Sucursales", backref="canales_de_venta", lazy=True)
    cuenta_de_banco_efectivo = db.relationship("CuentasDeBanco",foreign_keys=[id_cuenta_de_banco_efectivo], backref="sucursales_efectivo", lazy="joined")
    cuenta_de_banco_terminal = db.relationship("CuentasDeBanco",foreign_keys=[id_cuenta_de_banco_terminal], backref="sucursales_terminal", lazy="joined")

class Comisiones(db.Model,BaseMixin,AuditMixin):

    id_sucursal = db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=False) 
    id_canal_de_venta = db.Column(db.UUID, db.ForeignKey("canales_de_venta.id"), nullable=True)
    id_cuenta_de_banco = db.Column(db.UUID, db.ForeignKey("cuentas_de_banco.id"), nullable=True)

    comision_porcentaje_total = db.Column(db.Float, nullable=False)
    estatus = db.Column(db.String(255),default="Activo")

    sucursal = db.relationship("Sucursales", backref="comisiones", lazy=True)
    canal_de_venta = db.relationship("CanalesDeVenta", backref="comisiones", lazy=True)
    cuenta_de_banco = db.relationship("CuentasDeBanco", backref="comisiones", lazy=True)

    @validates('comision_porcentaje_total')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value

class AreasDeSucursales(db.Model,BaseMixin,AuditMixin):
    
    id_sucursal=db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=True)

    nombre=db.Column(db.String(255), nullable=False)
    numero_de_mesas=db.Column(db.Integer, nullable=True)
    estatus = db.Column(db.String(255),default="Activo")

    sucursal = db.relationship("Sucursales", backref="areas_de_sucursales", lazy=True)

class Mesas(db.Model,BaseMixin,AuditMixin):
    
    id_sucursal=db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=True)
    id_area_de_sucursal=db.Column(db.UUID, db.ForeignKey("areas_de_sucursales.id"), nullable=True)

    numero_de_mesa = db.Column(db.Integer, nullable=True)
    numero_de_comensales = db.Column(db.Integer, nullable=True)
    estatus = db.Column(db.String(255),default="Activo")
    estatus_actual = db.Column(db.String(255),default="Disponible")

    sucursal = db.relationship("Sucursales", backref="mesas", lazy=True)
    area_de_sucursal = db.relationship("AreasDeSucursales", backref="mesas", lazy=True)

class RazonesDeCancelacion(db.Model,BaseMixin,AuditMixin):

    razon = db.Column(db.String(255))
    estatus = db.Column(db.String(255),default="Activo")
