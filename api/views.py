from rest_framework import generics, status, viewsets, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group
from talleres.models import Taller, Categoria, Lugar, Profesor
from .serializers import TallerSerializer, TallerCreateSerializer
from .permissions import EsJuntaVecinosPermission, PuedeEditarTallerPermission
from externos.services import FeriadosService


class TallerViewSet(viewsets.ModelViewSet):
    """
    ViewSet completo para gestión de talleres via API
    REQ04: Las Juntas de Vecinos pueden proponer nuevos talleres
    REQ05: Las Juntas de Vecinos pueden ver todos los talleres
    """
    permission_classes = [IsAuthenticated, EsJuntaVecinosPermission, PuedeEditarTallerPermission]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titulo', 'descripcion', 'categoria__nombre', 'profesor__nombre', 'profesor__apellido']
    ordering_fields = ['fecha', 'fecha_creacion', 'titulo', 'precio']
    ordering = ['-fecha_creacion']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TallerCreateSerializer
        return TallerSerializer
    
    def get_queryset(self):
        """
        REQ05: Mostrar todos los talleres sin importar su estado
        """
        queryset = Taller.objects.all().select_related(
            'categoria', 'profesor', 'lugar', 'creado_por'
        )
        
        # Filtros adicionales por query parameters
        estado = self.request.query_params.get('estado', None)
        categoria = self.request.query_params.get('categoria', None)
        mis_talleres = self.request.query_params.get('mis_talleres', None)
        
        if estado:
            queryset = queryset.filter(estado=estado)
        
        if categoria:
            queryset = queryset.filter(categoria__id=categoria)
        
        if mis_talleres and mis_talleres.lower() == 'true':
            queryset = queryset.filter(creado_por=self.request.user)
        
        return queryset
    
    def perform_create(self, serializer):
        """
        REQ04: Crear taller asignando usuario creador
        La validación de feriados se hace en el serializer
        """
        serializer.save(creado_por=self.request.user)
    
    @action(detail=False, methods=['get'])
    def mis_talleres(self, request):
        """
        Endpoint adicional para que las JJVV vean solo sus talleres propuestos
        """
        talleres = self.get_queryset().filter(creado_por=request.user)
        page = self.paginate_queryset(talleres)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(talleres, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """
        Endpoint para obtener estadísticas de talleres
        """
        queryset = self.get_queryset()
        stats = {
            'total_talleres': queryset.count(),
            'talleres_pendientes': queryset.filter(estado='pendiente').count(),
            'talleres_aceptados': queryset.filter(estado='aceptado').count(),
            'talleres_rechazados': queryset.filter(estado='rechazado').count(),
            'mis_talleres': queryset.filter(propuesto_por=request.user).count(),
            'categorias_usadas': queryset.values('categoria__nombre').distinct().count(),
        }
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def proximos(self, request):
        """
        Endpoint para obtener talleres próximos (aceptados y futuros)
        """
        from django.utils import timezone
        talleres = self.get_queryset().filter(
            estado='aceptado',
            fecha_inicio__gte=timezone.now().date()
        ).order_by('fecha_inicio')[:10]
        
        serializer = self.get_serializer(talleres, many=True)
        return Response(serializer.data)


# Mantener la clase original para compatibilidad
class TallerListCreateView(generics.ListCreateAPIView):
    """
    REQ04: Las Juntas de Vecinos pueden proponer nuevos talleres
    REQ05: Las Juntas de Vecinos pueden ver todos los talleres
    """
    permission_classes = [IsAuthenticated, EsJuntaVecinosPermission]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TallerCreateSerializer
        return TallerSerializer
    
    def get_queryset(self):
        """
        REQ05: Mostrar todos los talleres sin importar su estado
        """
        return Taller.objects.all().select_related(
            'categoria', 'profesor', 'lugar', 'propuesto_por'
        ).order_by('-fecha_creacion')
    
    def perform_create(self, serializer):
        """
        REQ04: Crear taller con estado pendiente y validación de feriados
        """
        taller = serializer.save(
            propuesto_por=self.request.user,
            estado='pendiente'
        )
        
        # REQ06: Validar feriados
        validacion = FeriadosService.validar_fecha_taller(
            taller.fecha_inicio, 
            taller.categoria.nombre
        )
        
        if not validacion['es_valido']:
            taller.estado = validacion['estado']
            taller.observaciones = validacion['observacion']
            taller.save()
        """
        REQ04: Crear taller con estado pendiente y validación de feriados
        """
        taller = serializer.save(
            propuesto_por=self.request.user,
            estado='pendiente'
        )
        
        # REQ06: Validar feriados
        validacion = FeriadosService.validar_fecha_taller(
            taller.fecha_inicio, 
            taller.categoria.nombre
        )
        
        if not validacion['es_valido']:
            taller.estado = validacion['estado']
            taller.observaciones = validacion['observacion']
            taller.save()


class TallerDetailView(generics.RetrieveAPIView):
    """
    Detalle de un taller específico para Juntas de Vecinos
    """
    serializer_class = TallerSerializer
    permission_classes = [IsAuthenticated, EsJuntaVecinosPermission]
    
    def get_queryset(self):
        return Taller.objects.all().select_related(
            'categoria', 'profesor', 'lugar', 'propuesto_por'
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated, EsJuntaVecinosPermission])
def categorias_list(request):
    """
    Lista de categorías disponibles para crear talleres
    """
    categorias = Categoria.objects.filter(activa=True).values('id', 'nombre', 'descripcion')
    return Response(list(categorias))


@api_view(['GET'])
@permission_classes([IsAuthenticated, EsJuntaVecinosPermission])
def lugares_list(request):
    """
    Lista de lugares disponibles para crear talleres
    """
    lugares = Lugar.objects.filter(activo=True).values(
        'id', 'nombre', 'direccion', 'capacidad_maxima'
    )
    return Response(list(lugares))


@api_view(['GET'])
@permission_classes([IsAuthenticated, EsJuntaVecinosPermission])
def profesores_list(request):
    """
    Lista de profesores disponibles para crear talleres
    """
    profesores = Profesor.objects.filter(activo=True).values(
        'id', 'nombre', 'apellido', 'especialidad'
    )
    return Response(list(profesores))


@api_view(['POST'])
@permission_classes([IsAuthenticated, EsJuntaVecinosPermission])
def validar_fecha_feriado(request):
    """
    Endpoint para validar si una fecha es feriado
    """
    fecha_str = request.data.get('fecha')
    categoria_nombre = request.data.get('categoria_nombre', '')
    
    if not fecha_str:
        return Response(
            {'error': 'Se requiere el parámetro fecha'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        from datetime import datetime
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except ValueError:
        return Response(
            {'error': 'Formato de fecha inválido. Use YYYY-MM-DD'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    validacion = FeriadosService.validar_fecha_taller(fecha, categoria_nombre)
    
    return Response({
        'fecha': fecha_str,
        'es_feriado': FeriadosService.es_feriado(fecha),
        'es_feriado_irrenunciable': FeriadosService.es_feriado_irrenunciable(fecha),
        'validacion': validacion
    })
