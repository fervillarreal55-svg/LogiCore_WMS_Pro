import csv
import json
from django.http import HttpResponse
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from .models import Almacen, Categoria, Producto, Recepcion, Despacho, PerfilUsuario, Trazabilidad

def exportar_a_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename=reporte_{meta.verbose_name_plural}.csv'
    
    writer = csv.writer(response)
    writer.writerow(field_names)
    
    for obj in queryset:
        writer.writerow([str(getattr(obj, field)) for field in field_names])
        
    return response

exportar_a_csv.short_description = "Descargar reporte seleccionado en Excel (CSV)"

def exportar_a_pdf(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=reporte_{meta.verbose_name_plural}.pdf'
    
    doc = SimpleDocTemplate(response, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=colors.HexColor('#2e7d32'),
        spaceAfter=15,
        alignment=1 
    )
    
    elements.append(Paragraph(f"Reporte de {meta.verbose_name_plural.capitalize()}", title_style))
    elements.append(Spacer(1, 10))
    
    field_names = [field.name for field in meta.fields]
    data = [field_names]
    
    for obj in queryset:
        data.append([str(getattr(obj, field)) for field in field_names])
        
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e7d32')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f1f8f2')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#c8e6c9')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ]))
    
    elements.append(table)
    doc.build(elements)
    return response

exportar_a_pdf.short_description = "Descargar reporte seleccionado en PDF"

@admin.register(Almacen)
class AlmacenAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'ubicacion')
    search_fields = ('nombre', 'ubicacion')
    actions = [exportar_a_csv, exportar_a_pdf]

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    actions = [exportar_a_csv, exportar_a_pdf]

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo_barras', 'nombre', 'categoria', 'almacen', 'stock', 'precio', 'ver_barcode')
    search_fields = ('nombre', 'codigo_barras')
    list_filter = ('categoria', 'almacen')
    readonly_fields = ('ver_barcode_grande',)
    actions = [exportar_a_csv, exportar_a_pdf]

    def ver_barcode(self, obj):
        if obj.codigo_barras:
            url = f"https://barcodeapi.org/api/128/{obj.codigo_barras}"
            return format_html('<img src="{}" height="30" alt="Barcode" />', url)
        return "Sin código"
    ver_barcode.short_description = 'Código de Barras'

    def ver_barcode_grande(self, obj):
        if obj.codigo_barras:
            url = f"https://barcodeapi.org/api/128/{obj.codigo_barras}"
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={obj.codigo_barras}"
            return format_html(
                '<div style="text-align: left;">'
                '<p><b>Código de Barras:</b><br><img src="{}" height="60" alt="Barcode"/></p>'
                '<p><b>Código QR:</b><br><img src="{}" width="120" height="120" alt="QR"/></p>'
                '</div>', 
                url, qr_url
            )
        return "Guarda el producto para generar los códigos."
    ver_barcode_grande.short_description = 'Vista previa de Códigos'

@admin.register(Recepcion)
class RecepcionAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'cantidad', 'proveedor', 'fecha_ingreso')
    list_filter = ('fecha_ingreso',)
    actions = [exportar_a_csv, exportar_a_pdf]

@admin.register(Despacho)
class DespachoAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'cantidad', 'destino', 'fecha_despacho')
    search_fields = ('destino',)
    actions = [exportar_a_csv, exportar_a_pdf]

@admin.register(Trazabilidad)
class TrazabilidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'ubicacion_actual', 'latitud', 'longitud', 'fecha_actualizacion')
    search_fields = ('ubicacion_actual', 'producto__nombre')
    list_filter = ('fecha_actualizacion',)
    actions = [exportar_a_csv, exportar_a_pdf]
    change_list_template = 'admin/modulo/trazabilidad/change_list.html'

    def changelist_view(self, request, extra_context=None):
        trazabilidades = Trazabilidad.objects.all()
        puntos = []
        for t in trazabilidades:
            if t.latitud and t.longitud:
                puntos.append({
                    'producto': t.producto.nombre if hasattr(t.producto, 'nombre') else str(t.producto),
                    'ubicacion': t.ubicacion_actual,
                    'lat': float(t.latitud),
                    'lng': float(t.longitud),
                    'fecha': str(t.fecha_actualizacion)
                })
        
        extra_context = extra_context or {}
        extra_context['puntos_mapa'] = json.dumps(puntos)
        return super().changelist_view(request, extra_context=extra_context)

class LogiCoreAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total_productos'] = Producto.objects.count()
        extra_context['almacenes_activos'] = Almacen.objects.count()
        extra_context['total_recepciones'] = Recepcion.objects.count()
        extra_context['total_despachos'] = Despacho.objects.count()
        
        productos = Producto.objects.all()[:10]
        extra_context['nombres_productos'] = [p.nombre for p in productos]
        extra_context['stocks_productos'] = [p.stock for p in productos]
        
        return super().index(request, extra_context)

admin.site.__class__ = LogiCoreAdminSite