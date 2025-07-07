from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone


class Categoria(models.Model):
    """
    Categorías de talleres (ej: Aire Libre, Deportes, Arte, etc.)
    """
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Lugar(models.Model):
    """
    Lugares donde se realizan los talleres
    """
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=300)
    capacidad_maxima = models.PositiveIntegerField()
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Lugar"
        verbose_name_plural = "Lugares"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.direccion}"


class Profesor(models.Model):
    """
    Profesores/Instructores de los talleres
    """
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(
        max_length=12,
        unique=True,
        validators=[RegexValidator(
            regex=r'^\d{7,8}-[0-9kK]$',
            message='RUT debe tener formato 12345678-9'
        )]
    )
    email = models.EmailField()
    telefono = models.CharField(max_length=15, blank=True)
    especialidad = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"
        ordering = ['apellido', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"


class Taller(models.Model):
    """
    Talleres comunitarios
    """
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)
    
    fecha = models.DateField(verbose_name="Fecha del taller")
    hora_inicio = models.TimeField(default='10:00')
    duracion_horas = models.DecimalField(
        max_digits=4, 
        decimal_places=1, 
        verbose_name="Duración (horas)"
    )
    
    cupos_maximos = models.PositiveIntegerField(default=20)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='pendiente'
    )
    
    observacion = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    
    # Metadata
    creado_por = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='talleres_creados'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "Taller"
        verbose_name_plural = "Talleres"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.titulo} - {self.categoria}"
    
    @property
    def esta_activo(self):
        """
        Un taller está activo si está aceptado y su fecha es futura
        """
        return (self.estado == 'aceptado' and 
                self.fecha >= timezone.now().date())
    
    @property
    def es_visible_publicamente(self):
        """
        Un taller es visible públicamente si está aceptado y es futuro (REQ08)
        """
        return self.esta_activo
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Validar que la duración sea positiva
        if self.duracion_horas <= 0:
            raise ValidationError('La duración debe ser mayor a 0 horas')
        
        # Validar que los cupos no excedan la capacidad del lugar
        if self.lugar and self.cupos_maximos > self.lugar.capacidad_maxima:
            raise ValidationError(
                f'Los cupos máximos ({self.cupos_maximos}) no pueden exceder '
                f'la capacidad del lugar ({self.lugar.capacidad_maxima})'
            )
        
        # Validar que la fecha no sea en el pasado (solo para nuevos talleres)
        if not self.pk:  # Solo para nuevos talleres
            from django.utils import timezone
            if self.fecha < timezone.now().date():
                raise ValidationError('La fecha del taller no puede ser en el pasado')
    
    def save(self, *args, **kwargs):
        """
        Sobrescribir save para aplicar validaciones automáticas
        """
        # Ejecutar validaciones
        self.full_clean()
        
        # Validar feriados automáticamente si es un taller nuevo o si se cambia la fecha
        validar_feriados = not self.pk or (
            self.pk and 
            Taller.objects.filter(pk=self.pk).exclude(fecha=self.fecha).exists()
        )
        
        if validar_feriados:
            try:
                from externos.services import FeriadosService
                validacion = FeriadosService.validar_fecha_taller(
                    self.fecha, 
                    self.categoria.nombre if self.categoria else ""
                )
                
                if not validacion['es_valido']:
                    self.estado = validacion['estado']
                    if not self.observacion:
                        self.observacion = validacion['observacion']
                    elif validacion['observacion'] not in self.observacion:
                        self.observacion += f" | {validacion['observacion']}"
            except Exception:
                # Si hay error en validación de feriados, continuar
                pass
        
        super().save(*args, **kwargs)
