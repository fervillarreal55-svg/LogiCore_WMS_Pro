from django.db import migrations

def crear_trazabilidades_iniciales(apps, schema_editor):
    Trazabilidad = apps.get_model('modulo', 'Trazabilidad')
    Producto = apps.get_model('modulo', 'Producto')
    
    producto_ejemplo = Producto.objects.first()
    
    if producto_ejemplo:
        Trazabilidad.objects.get_or_create(
            producto=producto_ejemplo,
            ubicacion_actual="Almacén Central UPEC - Tulcán",
            defaults={
                'latitud': 0.805500,
                'longitud': -77.734100,
                'observaciones': 'Ubicación inicial automática del Almacén Central'
            }
        )
        
        Trazabilidad.objects.get_or_create(
            producto=producto_ejemplo,
            ubicacion_actual="Centro de Distribución Norte - Ibarra",
            defaults={
                'latitud': 0.351700,
                'longitud': -78.122300,
                'observaciones': 'Ubicación automática del Centro de Distribución'
            }
        )

class Migration(migrations.Migration):

    dependencies = [
        ('modulo', '0005_trazabilidad'),
    ]

    operations = [
        migrations.RunPython(crear_trazabilidades_iniciales),
    ]