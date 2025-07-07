from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from .models import Categoria, Lugar, Profesor, Taller


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activa', 'descripcion']
    list_filter = ['activa']
    search_fields = ['nombre']
    list_editable = ['activa']


@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'direccion', 'capacidad_maxima', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre', 'direccion']
    list_editable = ['activo']


@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'rut', 'email', 'especialidad', 'activo']
    list_filter = ['activo', 'especialidad']
    search_fields = ['nombre', 'apellido', 'rut', 'email']
    list_editable = ['activo']
    
    def nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido}"
    nombre_completo.short_description = "Nombre Completo"


@admin.register(Taller)
class TallerAdmin(admin.ModelAdmin):
    list_display = [
        'titulo', 'categoria', 'profesor', 'lugar', 
        'fecha', 'estado_badge', 'creado_por'
    ]
    list_filter = [
        'estado', 'categoria', 'fecha', 'lugar', 'profesor'
    ]
    search_fields = ['titulo', 'descripcion']
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'descripcion', 'categoria')
        }),
        ('Recursos', {
            'fields': ('profesor', 'lugar')
        }),
        ('Programación', {
            'fields': (
                'fecha',
                'hora_inicio',
                'duracion_horas',
                'cupos_maximos', 
                'precio'
            )
        }),
        ('Estado y Observaciones', {
            'fields': ('estado', 'observacion')
        }),
        ('Metadata', {
            'fields': ('creado_por', 'fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']
    
    def estado_badge(self, obj):
        colors = {
            'pendiente': 'orange',
            'aceptado': 'green',
            'rechazado': 'red'
        }
        color = colors.get(obj.estado, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_badge.short_description = "Estado"
    
    def save_model(self, request, obj, form, change):
        # Si es un nuevo taller, asignar el usuario actual como creado_por
        if not change:
            obj.creado_por = request.user
        
        # Validar feriados antes de guardar (REQ06)
        try:
            from externos.services import FeriadosService
            
            if FeriadosService.es_feriado_irrenunciable(obj.fecha):
                obj.estado = 'rechazado'
                obj.observacion = "No se programan talleres en feriados irrenunciables"
                messages.warning(
                    request, 
                    f"El taller fue marcado como rechazado porque {obj.fecha} es un feriado irrenunciable."
                )
            elif FeriadosService.es_feriado(obj.fecha) and obj.categoria.nombre != "Aire Libre":
                obj.estado = 'rechazado'
                obj.observacion = "Solo se permiten talleres de categoría 'Aire Libre' en feriados"
                messages.warning(
                    request,
                    f"El taller fue marcado como rechazado porque {obj.fecha} es feriado y la categoría no es 'Aire Libre'."
                )
        except ImportError:
            # Si hay error en el import, continuar sin validación de feriados
            pass
        
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'categoria', 'profesor', 'lugar', 'creado_por'
        )
