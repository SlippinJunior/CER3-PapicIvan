from django.contrib import admin
from .models import FeriadoCache


@admin.register(FeriadoCache)
class FeriadoCacheAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'nombre', 'irrenunciable', 'tipo', 'fecha_consulta']
    list_filter = ['irrenunciable', 'tipo']
    search_fields = ['nombre']
    date_hierarchy = 'fecha'
    readonly_fields = ['fecha_consulta']
    
    actions = ['actualizar_feriados']
    
    def actualizar_feriados(self, request, queryset):
        """
        Acción para actualizar feriados desde la API
        """
        from .services import FeriadosService
        from django.core.cache import cache
        
        años = set(feriado.fecha.year for feriado in queryset)
        
        for año in años:
            # Limpiar cache
            cache.delete(f'feriados_{año}')
            # Forzar actualización
            FeriadosService.obtener_feriados_año(año)
        
        self.message_user(
            request,
            f"Se actualizaron los feriados para los años: {', '.join(map(str, años))}"
        )
    
    actualizar_feriados.short_description = "Actualizar feriados desde API"
