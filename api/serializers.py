from rest_framework import serializers
from django.contrib.auth.models import User
from talleres.models import Taller, Categoria, Lugar, Profesor


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']


class LugarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lugar
        fields = ['id', 'nombre']


class ProfesorSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.ReadOnlyField()
    
    class Meta:
        model = Profesor
        fields = ['id', 'nombre_completo']


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para mostrar información básica del usuario
    """
    nombre_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'nombre_completo', 'email']
    
    def get_nombre_completo(self, obj):
        return obj.get_full_name() or obj.username


class TallerSerializer(serializers.ModelSerializer):
    """
    Serializer para mostrar talleres según Anexo 5
    """
    categoria = CategoriaSerializer(read_only=True)
    lugar = LugarSerializer(read_only=True)
    profesor = ProfesorSerializer(read_only=True)
    
    class Meta:
        model = Taller
        fields = [
            'id', 
            'titulo', 
            'fecha', 
            'duracion_horas', 
            'estado', 
            'profesor', 
            'lugar', 
            'categoria', 
            'observacion'
        ]

class TallerCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear talleres (REQ04)
    """
    # Campos de solo lectura que se calculan automáticamente
    estado = serializers.CharField(read_only=True)
    observacion = serializers.CharField(read_only=True)
    
    class Meta:
        model = Taller
        fields = [
            'id', 'titulo', 'descripcion', 'categoria', 'profesor', 'lugar',
            'fecha', 'hora_inicio', 'duracion_horas', 'cupos_maximos', 'precio',
            'estado', 'observacion'
        ]
    
    def validate(self, data):
        """
        Validaciones personalizadas
        """
        # Validar que los cupos no excedan la capacidad del lugar
        if data['cupos_maximos'] > data['lugar'].capacidad_maxima:
            raise serializers.ValidationError(
                f"Los cupos máximos ({data['cupos_maximos']}) no pueden exceder "
                f"la capacidad del lugar ({data['lugar'].capacidad_maxima})"
            )
        
        # Validar que la categoría esté activa
        if not data['categoria'].activa:
            raise serializers.ValidationError(
                "No se pueden crear talleres en categorías inactivas"
            )
        
        # Validar que el lugar esté activo
        if not data['lugar'].activo:
            raise serializers.ValidationError(
                "No se pueden crear talleres en lugares inactivos"
            )
        
        # Validar que el profesor esté activo
        if not data['profesor'].activo:
            raise serializers.ValidationError(
                "No se pueden crear talleres con profesores inactivos"
            )
        
        return data
    
    def create(self, validated_data):
        """
        Crear taller con validación de feriados (REQ06)
        """
        # Validar feriados antes de crear
        try:
            from externos.services import FeriadosService
            
            fecha = validated_data['fecha']
            categoria_nombre = validated_data['categoria'].nombre
            
            validacion = FeriadosService.validar_fecha_taller(fecha, categoria_nombre)
            
            # Crear el taller con el estado determinado por la validación
            validated_data['estado'] = validacion['estado']
            validated_data['observacion'] = validacion['observacion']
            
        except ImportError:
            # Si hay error en el import, crear con estado pendiente
            validated_data['estado'] = 'pendiente'
            validated_data['observacion'] = ''
        
        return super().create(validated_data)
    
    def validate_fecha(self, value):
        """
        Validar que la fecha sea futura
        """
        from django.utils import timezone
        
        if value < timezone.now().date():
            raise serializers.ValidationError(
                "La fecha del taller no puede ser en el pasado"
            )
        
        return value
    
    def validate_cupos_maximos(self, value):
        """
        Validar que los cupos sean positivos
        """
        if value <= 0:
            raise serializers.ValidationError(
                "Los cupos máximos deben ser mayor a 0"
            )
        
        return value
    
    def validate_duracion_horas(self, value):
        """
        Validar que la duración sea positiva
        """
        if value <= 0:
            raise serializers.ValidationError(
                "La duración debe ser mayor a 0 horas"
            )
        
        return value
    
    def validate_precio(self, value):
        """
        Validar que el precio no sea negativo
        """
        if value < 0:
            raise serializers.ValidationError(
                "El precio no puede ser negativo"
            )
        
        return value


class TallerUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para actualizar talleres (solo campos permitidos)
    """
    
    class Meta:
        model = Taller
        fields = [
            'titulo', 'descripcion', 'fecha', 'hora_inicio', 
            'duracion_horas', 'cupos_maximos', 'precio'
        ]
    
    def validate(self, data):
        """
        Aplicar las mismas validaciones que en creación
        """
        # Reutilizar validaciones del serializer de creación
        create_serializer = TallerCreateSerializer()
        return create_serializer.validate(data)
