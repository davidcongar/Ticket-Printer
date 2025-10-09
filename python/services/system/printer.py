from escpos.printer import Usb
from datetime import datetime

def print_ticket(data):
    VENDOR_ID = 0x0483
    PRODUCT_ID = 0x5743

    printer=Usb(VENDOR_ID,PRODUCT_ID,timeout=0,in_ep=0x82,out_ep=0x01)
    restaurant = data.get("restaurant", "")
    address = data.get("address", "")
    order_items = data.get("items", [])
    discount = data.get("discount", 0.0)
    total = data.get("total", 0.0)
    canal_de_venta = data.get("sale_channel", "")

    # Start printing
    printer.set(align="center", bold=True, width=2, height=2)
    printer.text(restaurant + "\n")
    printer.set(align="center", bold=False, width=1, height=1)
    printer.text(address + "\n")
    printer.text(datetime.now().strftime("%Y-%m-%d %H:%M") + "\n")
    printer.text("--------------------------------\n")
    printer.set(align="left", bold=True)
    printer.text(f"Canal de venta: {canal_de_venta}\n")
    printer.text("--------------------------------\n")
    
    # Print order items
    printer.set(bold=False)
    line_width = 42  

    padding = 2       # extra right margin
    for item in order_items:
        name = item.get("name", "")
        notes=item.get("notes", "")
        qty = item.get("qty", 1)
        line_total = item.get("line_total", 0.0)

        # Left part = qty and name
        left_text = f"{qty} x {name}"
        right_text = f"${float(line_total):.2f}"

        # Pad so right_text stays away from edge
        line = f"{left_text:<{line_width - len(right_text) - padding}}{right_text}\n"
        printer.text(line)
        if notes:
                printer.text(f" {notes}\n")         

    printer.text("--------------------------------\n")

    # Totals (also padded to leave margin)
    printer.text(f"{'Descuento:':<{line_width - 10 - padding}}${float(discount):.2f}\n")
    printer.text(f"{'TOTAL:':<{line_width - 10 - padding}}${float(total):.2f}\n")
    printer.text("--------------------------------\n")

    # Footer
    printer.set(align="center", bold=True)
    printer.text("Gracias!\n")
    printer.text("Los Esperamos Pronto!\n\n\n")
    printer.cut()
    printer.close()

def print_ticket_kitchen(data):
    VENDOR_ID = 0x0483
    PRODUCT_ID = 0x5743

    printer=Usb(VENDOR_ID,PRODUCT_ID,timeout=0,in_ep=0x82,out_ep=0x01)
    restaurant = data.get("restaurant", "")
    order_items = data.get("items", [])
    canal_de_venta = data.get("sale_channel", "")
    hour_sent = data.get("hour_sent", "")

    # Start printing
    printer.set(align="center", bold=True, width=2, height=2)
    printer.text(restaurant + "\n")
    printer.set(align="center", bold=False, width=1, height=1)
    printer.text(datetime.now().strftime("%Y-%m-%d %H:%M") + "\n")
    printer.text("--------------------------------\n")
    printer.set(align="left", bold=True)
    printer.text(f"Canal de venta: {canal_de_venta}\n")
    printer.text(f"Hora: {hour_sent}\n")
    printer.text("--------------------------------\n")
    
    # Print order items
    printer.set(bold=True, width=3, height=3)
    line_width = 42  
    padding = 2 

    for item in order_items:
        name = item.get("name", "")
        notes=item.get("notes", "")
        qty = item.get("qty", 1)

        # Left part = qty and name
        left_text = f"{qty} x {name}"

        # Pad so right_text stays away from edge
        line = f"{left_text:<{line_width - padding}}\n"
        printer.text(line)
        if notes:
                printer.text(f" {notes}\n")        

    printer.text("--------------------------------\n")

    # Footer
    printer.set(align="center", bold=True)
    printer.cut()
    printer.close()
