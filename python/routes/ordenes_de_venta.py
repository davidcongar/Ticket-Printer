
from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for,session,request,render_template_string

from python.models import db
from python.models.modelos import *
from sqlalchemy.orm import joinedload
from sqlalchemy import String, Text, or_,func,desc
from datetime import date,timedelta
from python.services.system.printer import *
import os

ordenes_de_venta_bp = Blueprint("ordenes_de_venta", __name__,url_prefix="/ordenes_de_venta")


@ordenes_de_venta_bp.route("/print_ticket/<uuid:id>", methods=["GET"])
def ov_print_ticket(id):
    orden = OrdenesDeVenta.query.get(id)
    canal_de_venta = CanalesDeVenta.query.get(orden.id_canal_de_venta).nombre
    sucursal=Sucursales.query.get(os.getenv('ID_SUCURSAL'))
    empresa=Empresas.query.get(sucursal.id_empresa)
    cliente=Clientes.query.get(orden.id_cliente)
    productos = ProductosEnOrdenesDeVentas.query.filter_by(id_orden_de_venta=id).all()
    items = []
    for p in productos:
        nombre_prod=Menu.query.get(p.id_menu).nombre
        notas=p.notas + "," if p.notas else ""
        mods=p.modificaciones.strip("{}").replace('"', '') if p.modificaciones else ""
        mods = {x.strip() for x in mods.split(",")}
        mods = ",".join(sorted(mods))
        items.append({
            "name": nombre_prod,
            "notes": f'{notas}{mods}',
            "qty": str(round(p.cantidad,0)),
            "price": str(round(p.precio_unitario,2)),
            "line_total":str(round(p.cantidad*p.precio_unitario,2))
        })
        adicionales=ComplementosEnOrdenesDeVentas.query.filter_by(id_producto_en_orden_de_venta=p.id).all()
        for adicional in adicionales:
            items.append({
                "name": adicional.complemento_de_menu.nombre,
                "notes": '',
                "qty": str(round(adicional.cantidad,0)),
                "price": str(round(adicional.precio_unitario,2)),
                "line_total":str(round(adicional.cantidad*adicional.precio_unitario,2))
            })

    # Build payload for the printer
    payload = {
        "restaurant": sucursal.nombre,
        "client_name":cliente.nombre if cliente else None,
        "client_phone_number":cliente.telefono if cliente else None,
        "address": sucursal.direccion,
        "phone_number":sucursal.telefono,
        "sale_channel": canal_de_venta,
        "total": str(round(orden.importe_total,2)),
        "discount": str(round(orden.descuentos,2)),
        "items": items,
        "online_url":f'snappkitchen.snappsolutions.com/pedidos_en_linea/{sucursal.id_empresa}' if empresa.is_pedidos_en_linea==True else None,
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
    cliente=Clientes.query.get(record.id_cliente)
    sucursal=Sucursales.query.get(os.getenv('ID_SUCURSAL'))
    canal_de_venta = CanalesDeVenta.query.get(record.id_canal_de_venta).nombre
    productos = ProductosEnOrdenesDeVentas.query.filter_by(id_orden_de_venta=id).all()
    items = []
    for p in productos:
        nombre_prod=Menu.query.get(p.id_menu).nombre
        notas=p.notas + "," if p.notas else ""
        mods=p.modificaciones.strip("{}").replace('"', '') if p.modificaciones else ""
        mods = {x.strip() for x in mods.split(",")}
        mods = ",".join(sorted(mods))
        items.append({
            "name": nombre_prod,
            "notes": f'{notas}{mods}',
            "qty": str(round(p.cantidad,0))
        })
        adicionales=ComplementosEnOrdenesDeVentas.query.filter_by(id_producto_en_orden_de_venta=p.id).all()
        for adicional in adicionales:
            items.append({
                "name": adicional.complemento_de_menu.nombre,
                "notes": '',
                "qty": str(round(adicional.cantidad,0)),
                "price": str(round(adicional.precio_unitario,2)),
                "line_total":str(round(adicional.cantidad*adicional.precio_unitario,2))
            })        

    # Build payload for the printer
    payload = {
        "restaurant": sucursal.nombre,
        "client_name":cliente.nombre if cliente else None,
        "client_phone_number":cliente.telefono if cliente else None,        
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
