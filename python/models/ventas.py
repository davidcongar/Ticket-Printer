import uuid
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from python.models import db
from python.models.sistema import *
from datetime import date

class OrdenesDeVenta(db.Model,BaseMixin,AuditMixin):

    id_sucursal = db.Column(db.UUID, db.ForeignKey("sucursales.id"), nullable=True)
    id_canal_de_venta = db.Column(db.UUID, db.ForeignKey("canales_de_venta.id"), nullable=False) 
    id_cuenta_de_banco = db.Column(db.UUID, db.ForeignKey("cuentas_de_banco.id"), nullable=True) 

    fecha_venta = db.Column(db.Date, nullable=True,default=date.today)
    metodo_de_pago = db.Column(db.String(50))  # e.g., Efectivo, Tarjeta, Transferencia
    subtotal = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    costo_de_envio = db.Column(db.Numeric(15, 2), nullable=True, default=0.00)
    propina = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    descuentos = db.Column(db.Numeric(15, 2), default=0.00)
    importe_total = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    comisiones=db.Column(db.Numeric(15, 2), default=0.00)
    importe_final = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)

    notas = db.Column(db.Text)
    id_cliente = db.Column(db.UUID, db.ForeignKey("clientes.id"), nullable=True)
    fecha_hora_en_proceso= db.Column(db.DateTime, nullable=True)
    fecha_hora_preparada= db.Column(db.DateTime, nullable=True)
    fecha_hora_entregada= db.Column(db.DateTime, nullable=True)
    estatus = db.Column(db.String(255),default="En revisión") # e.g., En revisión, Aprobada,Cancelada
    requiere_factura = db.Column(db.String(255),default="No") 

    canal_de_venta = db.relationship("CanalesDeVenta", backref="ordenes_de_venta", lazy=True)
    cliente = db.relationship("Clientes", backref="ordenes_de_venta", lazy=True)
    sucursal = db.relationship("Sucursales", backref="ordenes_de_venta", lazy=True)
    cuenta_de_banco = db.relationship("CuentasDeBanco", backref="ordenes_de_venta", lazy=True)

    @validates('propina','importe_total','subtotal')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value
    
class ProductosEnOrdenesDeVentas(db.Model,BaseMixin,AuditMixin):

    id_orden_de_venta = db.Column(db.UUID, db.ForeignKey("ordenes_de_venta.id"), nullable=False)
    id_menu = db.Column(db.UUID, db.ForeignKey("menu.id"), nullable=True)

    cantidad = db.Column(db.Numeric(15, 3), nullable=False, default=0)
    precio_unitario = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    subtotal = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    descuento_porcentaje = db.Column(db.Numeric(15, 2), default=0.00)
    importe_total = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    fecha_hora_en_proceso = db.Column(db.DateTime, nullable=True)
    fecha_hora_preparada = db.Column(db.DateTime, nullable=True)
    notas = db.Column(db.Text)
    razon_cancelacion = db.Column(db.String(255))
    modificaciones = db.Column(db.Text, nullable=True)
    estatus = db.Column(db.String(255),default="En espera")

    orden_de_venta = db.relationship("OrdenesDeVenta", backref="productos_en_ordenes_de_venta", lazy=True)
    menu = db.relationship("Menu", backref="productos_en_ordenes_de_venta", lazy=True)

    @validates('cantidad','precio_unitario','subtotal','descuento_porcentaje','importe_total')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value

class ComplementosEnOrdenesDeVentas(db.Model,BaseMixin,AuditMixin):

    id_orden_de_venta = db.Column(db.UUID, db.ForeignKey("ordenes_de_venta.id"), nullable=False)
    id_producto_en_orden_de_venta=db.Column(db.UUID, db.ForeignKey("productos_en_ordenes_de_ventas.id"), nullable=False)
    id_complemento_de_menu = db.Column(db.UUID, db.ForeignKey("complementos_de_menu.id"), nullable=True)

    cantidad = db.Column(db.Numeric(15, 3), nullable=False, default=0)
    precio_unitario = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    subtotal = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    descuento_porcentaje = db.Column(db.Numeric(15, 2), default=0.00)
    importe_total = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)

    orden_de_venta = db.relationship("OrdenesDeVenta", backref="complementos_en_ordenes_de_ventas", lazy=True)
    producto_en_orden_de_venta = db.relationship("ProductosEnOrdenesDeVentas", backref="complementos_en_ordenes_de_ventas", lazy=True)
    complemento_de_menu = db.relationship("ComplementosDeMenu", backref="complementos_en_ordenes_de_ventas", lazy=True)

    @validates('cantidad','precio_unitario','subtotal','descuento_porcentaje','importe_total')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value
    
class RecetasUtilizadasEnOrdenesDeVenta(db.Model,BaseMixin,AuditMixin):

    id_orden_de_venta = db.Column(db.UUID, db.ForeignKey("ordenes_de_venta.id"), nullable=False)
    id_producto_en_orden_de_venta = db.Column(db.UUID, db.ForeignKey("productos_en_ordenes_de_ventas.id"), nullable=True)
    id_complemento_en_orden_de_venta = db.Column(db.UUID, db.ForeignKey("complementos_en_ordenes_de_ventas.id"), nullable=True)
    id_producto=db.Column(db.UUID, db.ForeignKey("productos.id"), nullable=False)

    cantidad = db.Column(db.Numeric(15, 3), nullable=False, default=0)

    orden_de_venta = db.relationship("OrdenesDeVenta", backref="recetas_utilizadas_en_ordenes_de_venta", lazy=True)
    producto_en_orden_de_venta = db.relationship("ProductosEnOrdenesDeVentas", backref="recetas_utilizadas_en_ordenes_de_venta", lazy=True)
    complemento_en_orden_de_venta = db.relationship("ComplementosEnOrdenesDeVentas", backref="recetas_utilizadas_en_ordenes_de_venta", lazy=True)
    producto = db.relationship("Productos", backref="recetas_utilizadas_en_ordenes_de_venta", lazy=True)

class PedidosEnLinea(db.Model,BaseMixin):

    id_orden_de_venta = db.Column(db.UUID, db.ForeignKey("ordenes_de_venta.id"), nullable=True)
    id_cliente=db.Column(db.UUID, db.ForeignKey("clientes.id"), nullable=True)

    id_sucursal = db.Column(db.UUID, db.ForeignKey("sucursales.id"))
    nombre = db.Column(db.String(50), nullable=True)
    telefono = db.Column(db.String(50), nullable=True)
    correo_electronico = db.Column(db.String(50), nullable=True)
    direccion = db.Column(db.String(255), nullable=True)
    numero_exterior = db.Column(db.String(10), nullable=True)
    numero_interior = db.Column(db.String(10), nullable=True)
    instrucciones_de_entrega = db.Column(db.String(255), nullable=True)
    metodo_de_pago=db.Column(db.String(50), nullable=True)
    fecha_hora_ordenado=db.Column(db.DateTime, nullable=True)
    subtotal=db.Column(db.Float, nullable=True,default=0)
    propina=db.Column(db.Float, nullable=True,default=0)
    importe_total=db.Column(db.Float, nullable=True,default=0)
    estatus = db.Column(db.String(255),default="Sin completar")
    id_empresa = db.Column(db.UUID, db.ForeignKey("empresas.id"))

    orden_de_venta = db.relationship("OrdenesDeVenta", backref="pedidos_en_linea", lazy=True)
    empresa = db.relationship("Empresas", backref="pedidos_en_linea", lazy=True)
    sucursal = db.relationship("Sucursales", backref="pedidos_en_linea", lazy=True)
    cliente = db.relationship("Clientes", backref="pedidos_en_linea", lazy=True)

class ProductosEnPedidosEnLinea(db.Model,BaseMixin):

    id_pedido_en_linea = db.Column(db.UUID, db.ForeignKey("pedidos_en_linea.id"), nullable=False)
    id_menu = db.Column(db.UUID, db.ForeignKey("menu.id"), nullable=False)
    id_empresa = db.Column(db.UUID, db.ForeignKey("empresas.id"), nullable=False)

    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    subtotal = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    modificaciones = db.Column(db.Text, nullable=True)
    notas = db.Column(db.Text, nullable=True)

    empresa = db.relationship("Empresas", backref="productos_en_pedidos_en_linea", lazy=True)
    pedido_en_linea = db.relationship("PedidosEnLinea", backref="productos_en_pedidos_en_linea", lazy=True)
    menu = db.relationship("Menu", backref="productos_en_pedidos_en_linea", lazy=True)

class ComplementosEnPedidosEnLinea(db.Model,BaseMixin):

    id_pedido_en_linea = db.Column(db.UUID, db.ForeignKey("pedidos_en_linea.id"), nullable=False)
    id_producto_en_pedido_en_linea = db.Column(db.UUID, db.ForeignKey("productos_en_pedidos_en_linea.id"), nullable=False)
    id_complemento_de_menu = db.Column(db.UUID, db.ForeignKey("complementos_de_menu.id"), nullable=False)
    id_empresa = db.Column(db.UUID, db.ForeignKey("empresas.id"), nullable=False)

    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    subtotal = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    notas = db.Column(db.Text, nullable=True)

    empresa = db.relationship("Empresas", backref="complementos_en_pedidos_en_linea", lazy=True)
    pedido_en_linea = db.relationship("PedidosEnLinea", backref="complementos_en_pedidos_en_linea", lazy=True)
    producto_en_pedido_en_linea = db.relationship("ProductosEnPedidosEnLinea", backref="complementos_en_pedidos_en_linea", lazy=True)
    complemento_de_menu = db.relationship("ComplementosDeMenu", backref="complementos_en_pedidos_en_linea", lazy=True)

class PedidosDeMesas(db.Model,BaseMixin,AuditMixin):

    id_sucursal = db.Column(db.UUID, db.ForeignKey("sucursales.id"))
    id_area_de_sucursal = db.Column(db.UUID, db.ForeignKey("areas_de_sucursales.id"))
    id_mesa = db.Column(db.UUID, db.ForeignKey("mesas.id"))
    id_orden_de_venta = db.Column(db.UUID, db.ForeignKey("ordenes_de_venta.id"), nullable=True)
    id_empleado = db.Column(db.UUID, db.ForeignKey("empleados.id"), nullable=True)

    fecha = db.Column(db.Date, nullable=True,default=date.today)
    numero_de_comensales = db.Column(db.Integer, nullable=False)
    alergias = db.Column(db.String(255), nullable=True)
    notas = db.Column(db.Text, nullable=True)
    estatus = db.Column(db.String(255),default="En proceso")

    orden_de_venta = db.relationship("OrdenesDeVenta", backref="pedidos_de_mesas", lazy=True)
    sucursal = db.relationship("Sucursales", backref="pedidos_de_mesas", lazy=True)
    mesa = db.relationship("Mesas", backref="pedidos_de_mesas", lazy=True)
    area_de_sucursal=db.relationship("AreasDeSucursales", backref="pedidos_de_mesas", lazy=True)
    empleado = db.relationship("Empleados", backref="pedidos_de_mesas", lazy=True)

class ProductosEnPedidosDeMesas(db.Model,BaseMixin,AuditMixin):

    id_pedido_de_mesa = db.Column(db.UUID, db.ForeignKey("pedidos_de_mesas.id"), nullable=False)
    id_menu = db.Column(db.UUID, db.ForeignKey("menu.id"), nullable=False)

    comensal=db.Column(db.String(10))
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_hora_en_proceso = db.Column(db.DateTime, nullable=True)
    fecha_hora_preparada = db.Column(db.DateTime, nullable=True)
    modificaciones = db.Column(db.Text, nullable=True)
    descuento_porcentaje = db.Column(db.Numeric(15, 2), default=0.00)
    notas = db.Column(db.Text, nullable=True)
    razon_cancelacion=db.Column(db.String(255))
    estatus = db.Column(db.String(255),default="En espera") # en espera, ordenado, preparado,cancelado

    pedido_de_mesa = db.relationship("PedidosDeMesas", backref="productos_en_pedidos_de_mesas", lazy=True)
    menu = db.relationship("Menu", backref="productos_en_pedidos_de_mesas", lazy=True)

class ComplementosEnPedidosDeMesas(db.Model,BaseMixin,AuditMixin):

    id_pedido_de_mesa = db.Column(db.UUID, db.ForeignKey("pedidos_de_mesas.id"), nullable=False)
    id_producto_en_pedido_de_mesa=db.Column(db.UUID, db.ForeignKey("productos_en_pedidos_de_mesas.id"), nullable=False)
    id_complemento_de_menu = db.Column(db.UUID, db.ForeignKey("complementos_de_menu.id"), nullable=False)

    cantidad = db.Column(db.Integer, nullable=False)
    descuento_porcentaje = db.Column(db.Numeric(15, 2), default=0.00)
    razon_cancelacion=db.Column(db.String(255))

    pedido_de_mesa = db.relationship("PedidosDeMesas", backref="complementos_en_pedidos_de_mesas", lazy=True)
    producto_en_pedido_de_mesa = db.relationship("ProductosEnPedidosDeMesas", backref="complementos_en_pedidos_de_mesas", lazy=True)
    complemento_de_menu = db.relationship("ComplementosDeMenu", backref="complementos_en_pedidos_de_mesas", lazy=True)