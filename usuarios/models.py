from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver


class PerfilUsuario(models.Model):
    """
    Perfil extendido para usuarios del sistema
    """
    TIPO_USUARIO_CHOICES = [
        ('administrador', 'Administrador'),
        ('funcionario', 'Funcionario Municipal'),
        ('junta_vecinos', 'Junta de Vecinos'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO_CHOICES,
        default='funcionario'
    )
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.CharField(max_length=300, blank=True)
    activo = models.BooleanField(default=True)
    
    # Campos específicos para Juntas de Vecinos
    nombre_junta = models.CharField(max_length=200, blank=True)
    sector = models.CharField(max_length=100, blank=True)
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_tipo_usuario_display()})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Asignar grupo según tipo de usuario
        self._asignar_grupo()
    
    def _asignar_grupo(self):
        """
        Asigna el grupo correspondiente según el tipo de usuario
        """
        # Remover de todos los grupos primero
        self.user.groups.clear()
        
        # Crear grupos si no existen
        grupos = {
            'administrador': 'Administradores',
            'funcionario': 'Funcionarios Municipales',
            'junta_vecinos': 'Juntas de Vecinos'
        }
        
        nombre_grupo = grupos.get(self.tipo_usuario)
        if nombre_grupo:
            grupo, created = Group.objects.get_or_create(name=nombre_grupo)
            self.user.groups.add(grupo)


@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """
    Crear perfil automáticamente cuando se crea un usuario
    """
    if created:
        PerfilUsuario.objects.create(user=instance)


@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    """
    Guardar perfil cuando se guarda el usuario
    """
    if hasattr(instance, 'perfilusuario'):
        instance.perfilusuario.save()
