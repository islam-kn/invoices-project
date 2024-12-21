# invoice_pdf.py
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from datetime import datetime
import os

class InvoicePDFGenerator:
    def __init__(self, invoice_data):
        self.invoice_data = invoice_data
        self.width, self.height = A4

    def generate(self, filename=None):
        if not filename:
            filename = f"invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        c = canvas.Canvas(filename, pagesize=A4)
        self._draw_header(c)
        self._draw_customer_info(c)
        self._draw_items_table(c)
        self._draw_totals(c)
        c.save()
        return filename

    def _draw_header(self, c):
        # Company logo/header
        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, self.height - 50, self.invoice_data['type'])
        c.setFont("Helvetica", 10)
        c.drawString(50, self.height - 70, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        c.drawString(50, self.height - 85, f"Invoice #: {self.invoice_data.get('invoice_id', '')}")

    def _draw_customer_info(self, c):
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, self.height - 120, "Customer Information")
        c.setFont("Helvetica", 10)
        c.drawString(50, self.height - 140, f"Company: {self.invoice_data['customer']['name']}")
        c.drawString(50, self.height - 155, f"Address: {self.invoice_data['customer']['address']}")
        c.drawString(50, self.height - 170, f"Phone: {self.invoice_data['customer']['phone']}")

    def _draw_items_table(self, c):
        # Table header
        y = self.height - 220
        headers = ["Product", "Quantity", "Unit Price", "Total"]
        x_positions = [50, 200, 300, 400]
        
        c.setFont("Helvetica-Bold", 10)
        for header, x in zip(headers, x_positions):
            c.drawString(x, y, header)
        
        # Table content
        c.setFont("Helvetica", 10)
        for item in self.invoice_data['items']:
            y -= 20
            c.drawString(x_positions[0], y, str(item['name']))
            c.drawString(x_positions[1], y, str(item['quantity']))
            c.drawString(x_positions[2], y, f"{item['price']:.2f}")
            c.drawString(x_positions[3], y, f"{item['total']:.2f}")

    def _draw_totals(self, c):
        y = self.height - 500
        c.setFont("Helvetica-Bold", 10)
        c.drawString(300, y, f"Net Total: {self.invoice_data['net_total']:.2f}")
        c.drawString(300, y - 20, f"Discount: {self.invoice_data['discount']}%")
        c.drawString(300, y - 40, f"Total: {self.invoice_data['total']:.2f}")