import requests
from datetime import datetime, date
from django.conf import settings
from django.core.cache import cache
from .models import FeriadoCache
import logging

logger = logging.getLogger(__name__)


class FeriadosService:
    """
    Servicio para consultar la API de feriados de Chile
    """
    
    @classmethod
    def es_feriado(cls, fecha):
        """
        Verifica si una fecha es feriado
        """
        feriados = cls.obtener_feriados_año(fecha.year)
        return any(f['fecha'] == fecha for f in feriados)
    
    @classmethod
    def es_feriado_irrenunciable(cls, fecha):
        """
        Verifica si una fecha es feriado irrenunciable
        """
        feriados = cls.obtener_feriados_año(fecha.year)
        for feriado in feriados:
            if feriado['fecha'] == fecha:
                return feriado.get('irrenunciable', False)
        return False
    
    @classmethod
    def obtener_feriados_año(cls, año):
        """
        Obtiene todos los feriados de un año específico
        """
        cache_key = f'feriados_{año}'
        feriados = cache.get(cache_key)
        
        if feriados is None:
            # Intentar obtener desde cache local (base de datos)
            feriados = cls._obtener_desde_cache_local(año)
            
            if not feriados:
                # Si no está en cache local, consultar API
                feriados = cls._consultar_api_feriados(año)
                cls._guardar_en_cache_local(feriados, año)
            
            # Guardar en cache de memoria por 1 hora
            cache.set(cache_key, feriados, 3600)
        
        return feriados
    
    @classmethod
    def _obtener_desde_cache_local(cls, año):
        """
        Obtiene feriados desde la base de datos local
        """
        try:
            feriados_cache = FeriadoCache.objects.filter(
                fecha__year=año
            ).values('fecha', 'nombre', 'irrenunciable', 'tipo')
            
            return [
                {
                    'fecha': f['fecha'],
                    'nombre': f['nombre'],
                    'irrenunciable': f['irrenunciable'],
                    'tipo': f['tipo']
                }
                for f in feriados_cache
            ]
        except Exception as e:
            logger.error(f"Error al obtener feriados desde cache local: {e}")
            return []
    
    @classmethod
    def _consultar_api_feriados(cls, año):
        """
        Consulta la API oficial de feriados de Chile
        """
        try:
            url = f"{settings.FERIADOS_API_URL}/{año}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            feriados_api = response.json()
            feriados = []
            
            for feriado in feriados_api:
                try:
                    fecha_str = feriado['fecha']
                    fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
                    
                    feriados.append({
                        'fecha': fecha_obj,
                        'nombre': feriado.get('nombre', ''),
                        'irrenunciable': feriado.get('irrenunciable', False),
                        'tipo': feriado.get('tipo', '')
                    })
                except (ValueError, KeyError) as e:
                    logger.warning(f"Error al procesar feriado {feriado}: {e}")
                    continue
            
            return feriados
            
        except requests.RequestException as e:
            logger.error(f"Error al consultar API de feriados: {e}")
            # Fallback: usar feriados hardcodeados para 2025
            return cls._obtener_feriados_fallback(año)
        except Exception as e:
            logger.error(f"Error inesperado al consultar feriados: {e}")
            return cls._obtener_feriados_fallback(año)
    
    @classmethod
    def _obtener_feriados_fallback(cls, año):
        """
        Feriados hardcodeados como fallback cuando la API no responde
        """
        feriados_por_año = {
            2025: [
                {'fecha': date(2025, 1, 1), 'nombre': 'Año Nuevo', 'irrenunciable': True, 'tipo': 'Irrenunciable'},
                {'fecha': date(2025, 5, 1), 'nombre': 'Día del Trabajador', 'irrenunciable': True, 'tipo': 'Irrenunciable'},
                {'fecha': date(2025, 5, 21), 'nombre': 'Día de las Glorias Navales', 'irrenunciable': True, 'tipo': 'Irrenunciable'},
                {'fecha': date(2025, 6, 29), 'nombre': 'San Pedro y San Pablo', 'irrenunciable': False, 'tipo': 'Civil'},
                {'fecha': date(2025, 7, 16), 'nombre': 'Virgen del Carmen', 'irrenunciable': False, 'tipo': 'Religioso'},
                {'fecha': date(2025, 9, 18), 'nombre': 'Independencia Nacional', 'irrenunciable': True, 'tipo': 'Irrenunciable'},
                {'fecha': date(2025, 9, 19), 'nombre': 'Día de las Glorias del Ejército', 'irrenunciable': True, 'tipo': 'Irrenunciable'},
                {'fecha': date(2025, 10, 31), 'nombre': 'Día de las Iglesias Evangélicas y Protestantes', 'irrenunciable': False, 'tipo': 'Religioso'},
                {'fecha': date(2025, 11, 1), 'nombre': 'Día de Todos los Santos', 'irrenunciable': False, 'tipo': 'Religioso'},
                {'fecha': date(2025, 12, 8), 'nombre': 'Inmaculada Concepción', 'irrenunciable': False, 'tipo': 'Religioso'},
                {'fecha': date(2025, 12, 25), 'nombre': 'Navidad', 'irrenunciable': True, 'tipo': 'Irrenunciable'}
            ],
            2026: [
                {'fecha': date(2026, 1, 1), 'nombre': 'Año Nuevo', 'irrenunciable': True, 'tipo': 'Irrenunciable'},
                {'fecha': date(2026, 5, 1), 'nombre': 'Día del Trabajador', 'irrenunciable': True, 'tipo': 'Irrenunciable'},
                {'fecha': date(2026, 5, 21), 'nombre': 'Día de las Glorias Navales', 'irrenunciable': True, 'tipo': 'Irrenunciable'},
                {'fecha': date(2026, 6, 29), 'nombre': 'San Pedro y San Pablo', 'irrenunciable': False, 'tipo': 'Civil'},
                {'fecha': date(2026, 7, 16), 'nombre': 'Virgen del Carmen', 'irrenunciable': False, 'tipo': 'Religioso'},
                {'fecha': date(2026, 9, 18), 'nombre': 'Independencia Nacional', 'irrenunciable': True, 'tipo': 'Irrenunciable'},
                {'fecha': date(2026, 9, 19), 'nombre': 'Día de las Glorias del Ejército', 'irrenunciable': True, 'tipo': 'Irrenunciable'},
                {'fecha': date(2026, 10, 31), 'nombre': 'Día de las Iglesias Evangélicas y Protestantes', 'irrenunciable': False, 'tipo': 'Religioso'},
                {'fecha': date(2026, 11, 1), 'nombre': 'Día de Todos los Santos', 'irrenunciable': False, 'tipo': 'Religioso'},
                {'fecha': date(2026, 12, 8), 'nombre': 'Inmaculada Concepción', 'irrenunciable': False, 'tipo': 'Religioso'},
                {'fecha': date(2026, 12, 25), 'nombre': 'Navidad', 'irrenunciable': True, 'tipo': 'Irrenunciable'}
            ]
        }
        
        return feriados_por_año.get(año, [])
    
    @classmethod
    def _guardar_en_cache_local(cls, feriados, año):
        """
        Guarda los feriados en la base de datos local para cache
        """
        try:
            # Eliminar feriados existentes del año
            FeriadoCache.objects.filter(fecha__year=año).delete()
            
            # Crear nuevos registros
            feriados_cache = []
            for feriado in feriados:
                feriados_cache.append(
                    FeriadoCache(
                        fecha=feriado['fecha'],
                        nombre=feriado['nombre'],
                        irrenunciable=feriado['irrenunciable'],
                        tipo=feriado['tipo']
                    )
                )
            
            FeriadoCache.objects.bulk_create(feriados_cache)
            logger.info(f"Se guardaron {len(feriados_cache)} feriados en cache local para el año {año}")
            
        except Exception as e:
            logger.error(f"Error al guardar feriados en cache local: {e}")
    
    @classmethod
    def validar_fecha_taller(cls, fecha, categoria_nombre):
        """
        Valida si se puede crear un taller en una fecha específica
        según las reglas de negocio (REQ06)
        
        Returns:
            dict: {
                'es_valido': bool,
                'estado': str,  # 'aceptado' o 'rechazado'
                'observacion': str
            }
        """
        if cls.es_feriado_irrenunciable(fecha):
            return {
                'es_valido': False,
                'estado': 'rechazado',
                'observacion': 'No se programan talleres en feriados irrenunciables'
            }
        
        if cls.es_feriado(fecha) and categoria_nombre != "Aire Libre":
            return {
                'es_valido': False,
                'estado': 'rechazado',
                'observacion': 'Solo se permiten talleres de categoría "Aire Libre" en feriados'
            }
        
        return {
            'es_valido': True,
            'estado': 'pendiente',
            'observacion': ''
        }
