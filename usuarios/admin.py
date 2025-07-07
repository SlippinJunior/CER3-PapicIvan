from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import PerfilUsuario


class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil'


class UsuarioPersonalizadoAdmin(UserAdmin):
    """
    Admin personalizado para Usuario que incluye el perfil
    """
    inlines = (PerfilUsuarioInline,)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('perfilusuario')


# Reemplazar el admin por defecto de User
admin.site.unregister(User)
admin.site.register(User, UsuarioPersonalizadoAdmin)


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'tipo_usuario', 'telefono', 'activo', 'nombre_junta'
    ]
    list_filter = ['tipo_usuario', 'activo', 'sector']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'nombre_junta']
    list_editable = ['activo']
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user', 'tipo_usuario', 'activo')
        }),
        ('Información de Contacto', {
            'fields': ('telefono', 'direccion')
        }),
        ('Información Junta de Vecinos', {
            'fields': ('nombre_junta', 'sector'),
            'classes': ('collapse',),
            'description': 'Solo completar si el tipo de usuario es Junta de Vecinos'
        })
    )
