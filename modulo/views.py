from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Almacen, Categoria, Producto, Recepcion, Despacho

@login_required
def dashboard_futurista(request):
    total_productos = Producto.objects.count()
    total_almacenes = Almacen.objects.count()
    total_recepciones = Recepcion.objects.count()
    total_despachos = Despacho.objects.count()
    
    # 10 productos tecnológicos para poblar el sistema
    productos = Producto.objects.all()[:10]
    almacenes = Almacen.objects.all()
    recepciones = Recepcion.objects.all()
    despachos = Despacho.objects.all()
    
    # Listas estructuradas para alimentar las gráficas dinámicas de Chart.js
    nombres_productos = [p.nombre for p in productos]
    stocks_productos = [p.stock for p in productos]

    context = {
        'total_productos': total_productos,
        'total_almacenes': total_almacenes,
        'total_recepciones': total_recepciones,
        'total_despachos': total_despachos,
        'productos': productos,
        'almacenes': almacenes,
        'recep_list': recepciones,
        'desp_list': despachos,
        'nombres_productos': nombres_productos,
        'stocks_productos': stocks_productos,
    }
    return render(request, 'admin/index.html', context)
def dashboard_invitado(request):
    total_productos = Producto.objects.count()
    total_almacenes = Almacen.objects.count()
    total_recepciones = Recepcion.objects.count()
    total_despachos = Despacho.objects.count()

    productos = Producto.objects.all()[:10]
    almacenes = Almacen.objects.all()
    recepciones = Recepcion.objects.all()
    despachos = Despacho.objects.all()

    contexto = {
        'total_productos': total_productos,
        'total_almacenes': total_almacenes,
        'total_recepciones': total_recepciones,
        'total_despachos': total_despachos,
        'productos': productos,
        'almacenes': almacenes,
        'recepciones': recepciones,
        'despachos': despachos,
    }
    return render(request, 'modulo/index.html', contexto)