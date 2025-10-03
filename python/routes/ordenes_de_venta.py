
from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for,session,request,render_template_string

from python.models import db
from python.models.modelos import *
from sqlalchemy.orm import joinedload
from sqlalchemy import String, Text, or_,func,desc
from datetime import date,timedelta
from python.services.system.printer import *


ordenes_de_venta_bp = Blueprint("ordenes_de_venta", __name__,url_prefix="/ordenes_de_venta")


@ordenes_de_venta_bp.route("/print_ticket/<uuid:id>", methods=["GET"])
def ov_print_ticket(id):
    orden = OrdenesDeVenta.query.get(id)
    canal_de_venta = CanalesDeVenta.query.get(orden.id_canal_de_venta).nombre
    sucursal=Sucursales.query.get(session['id_sucursal'])
    # Correct filter
    productos = ProductosEnOrdenesDeVentas.query.filter_by(id_orden_de_venta=id).all()

    # Build items list
    items = []
    for p in productos:
        nombre_prod=Menu.query.get(p.id_menu).nombre
        items.append({
            "name": nombre_prod,    # adjust field name
            "qty": str(round(p.cantidad,0)),           # adjust field name
            "price": str(round(p.precio_unitario,2)),   # adjust field name
            "line_total":str(round(p.cantidad*p.precio_unitario,2))
        })

    # Build payload for the printer
    payload = {
        "restaurant": sucursal.nombre,
        "restaurant": sucursal.direccion,
        "sale_channel": canal_de_venta,
        "total": str(round(orden.importe_total,2)),
        "discount": str(round(orden.descuentos,2)),
        "items": items
    }
    try:
        print_ticket(payload)
        message='El ticket se ha impreso.'
    except Exception as e:
        message=f'Hubo un error al imprimir el ticket: {e}'
    return render_template('main/print_alert.html',message=message)

@ordenes_de_venta_bp.route("/print_ticket_kitchen/<uuid:id>", methods=["GET"])
def ov_print_ticket_kitchen(id):
    record = OrdenesDeVenta.query.get(id)
    sucursal=Sucursales.query.get(session['id_sucursal'])
    canal_de_venta = CanalesDeVenta.query.get(record.id_canal_de_venta).nombre
    productos = ProductosEnOrdenesDeVentas.query.filter_by(id_orden_de_venta=id).all()
    items = []
    for p in productos:
        nombre_prod=Menu.query.get(p.id_menu).nombre
        items.append({
            "name": nombre_prod,
            "qty": str(round(p.cantidad,0))
        })

    # Build payload for the printer
    payload = {
        "restaurant": sucursal.nombre,
        "sale_channel": canal_de_venta,
        "hour_sent":datetime.now(),
        "items": items
    }
    try:
        print_ticket_kitchen(payload)
        message='El ticket para cocina se ha impreso.'
    except Exception as e:
        message=f'Hubo un error al imprimir el ticket: {e}'
    return render_template('main/print_alert.html',message=message)
