from rest_framework.permissions import BasePermission


class EsJuntaVecinosPermission(BasePermission):
    """
    Permiso personalizado para verificar que el usuario pertenece a Juntas de Vecinos
    """
    message = "Solo usuarios de Juntas de Vecinos pueden acceder a este recurso."
    
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.groups.filter(name='Juntas de Vecinos').exists())


class EsFuncionarioPermission(BasePermission):
    """
    Permiso para funcionarios municipales
    """
    message = "Solo funcionarios municipales pueden acceder a este recurso."
    
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                (request.user.groups.filter(name='Funcionarios Municipales').exists() or
                 request.user.is_staff))


class EsAdministradorPermission(BasePermission):
    """
    Permiso para administradores
    """
    message = "Solo administradores pueden acceder a este recurso."
    
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                (request.user.groups.filter(name='Administradores').exists() or
                 request.user.is_superuser))


class PuedeEditarTallerPermission(BasePermission):
    """
    Permiso para editar talleres - solo el creador o funcionarios
    """
    message = "Solo puedes editar talleres que hayas creado."
    
    def has_object_permission(self, request, view, obj):
        # Lectura permitida para todos los autenticados
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Edición solo para el creador o funcionarios/admin
        return (obj.propuesto_por == request.user or
                request.user.groups.filter(name__in=[
                    'Funcionarios Municipales', 
                    'Administradores'
                ]).exists() or
                request.user.is_staff or
                request.user.is_superuser)
