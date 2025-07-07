import django_filters
from django_filters import rest_framework as filters
from talleres.models import Taller, Categoria, Lugar, Profesor


class TallerFilter(django_filters.FilterSet):
    """
    Filtros avanzados para la API de talleres
    """
    categoria = filters.ModelChoiceFilter(queryset=Categoria.objects.filter(activa=True))
    lugar = filters.ModelChoiceFilter(queryset=Lugar.objects.filter(activo=True))
    profesor = filters.ModelChoiceFilter(queryset=Profesor.objects.filter(activo=True))
    estado = filters.ChoiceFilter(choices=Taller.ESTADO_CHOICES)
    
    # Filtros por fecha
    fecha_inicio_desde = filters.DateFilter(field_name='fecha_inicio', lookup_expr='gte')
    fecha_inicio_hasta = filters.DateFilter(field_name='fecha_inicio', lookup_expr='lte')
    fecha_fin_desde = filters.DateFilter(field_name='fecha_fin', lookup_expr='gte')
    fecha_fin_hasta = filters.DateFilter(field_name='fecha_fin', lookup_expr='lte')
    
    # Filtros por precio
    precio_min = filters.NumberFilter(field_name='precio', lookup_expr='gte')
    precio_max = filters.NumberFilter(field_name='precio', lookup_expr='lte')
    precio_gratuito = filters.BooleanFilter(method='filter_precio_gratuito')
    
    # Filtros por cupos
    cupos_min = filters.NumberFilter(field_name='cupos_maximos', lookup_expr='gte')
    cupos_max = filters.NumberFilter(field_name='cupos_maximos', lookup_expr='lte')
    
    # Filtro por usuario propietario
    mis_talleres = filters.BooleanFilter(method='filter_mis_talleres')
    
    # Filtros de texto
    nombre = filters.CharFilter(field_name='nombre', lookup_expr='icontains')
    descripcion = filters.CharFilter(field_name='descripcion', lookup_expr='icontains')
    
    class Meta:
        model = Taller
        fields = [
            'categoria', 'lugar', 'profesor', 'estado',
            'fecha_inicio_desde', 'fecha_inicio_hasta',
            'fecha_fin_desde', 'fecha_fin_hasta',
            'precio_min', 'precio_max', 'precio_gratuito',
            'cupos_min', 'cupos_max', 'mis_talleres',
            'nombre', 'descripcion'
        ]
    
    def filter_precio_gratuito(self, queryset, name, value):
        """
        Filtrar talleres gratuitos (precio = 0)
        """
        if value:
            return queryset.filter(precio=0)
        return queryset.filter(precio__gt=0)
    
    def filter_mis_talleres(self, queryset, name, value):
        """
        Filtrar talleres propuestos por el usuario actual
        """
        if value and self.request.user.is_authenticated:
            return queryset.filter(propuesto_por=self.request.user)
        return queryset
