from django.db import models


class FeriadoCache(models.Model):
    """
    Cache local de feriados para optimizar consultas a la API externa
    """
    fecha = models.DateField(unique=True)
    nombre = models.CharField(max_length=200)
    irrenunciable = models.BooleanField(default=False)
    tipo = models.CharField(max_length=50, blank=True)
    
    # Control de cache
    fecha_consulta = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Feriado (Cache)"
        verbose_name_plural = "Feriados (Cache)"
        ordering = ['fecha']
    
    def __str__(self):
        tipo_str = " (Irrenunciable)" if self.irrenunciable else ""
        return f"{self.fecha} - {self.nombre}{tipo_str}"
