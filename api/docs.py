from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.urls import reverse


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_documentation(request):
    """
    Endpoint que retorna la documentación de la API
    """
    base_url = request.build_absolute_uri('/api/v1/')
    
    documentation = {
        "titulo": "API Talleres Comunitarios - Municipalidad Villa Verde",
        "version": "1.0",
        "descripcion": "API REST para gestión de talleres comunitarios por Juntas de Vecinos",
        "autenticacion": {
            "tipo": "Token Authentication",
            "endpoint_token": request.build_absolute_uri('/api-token-auth/'),
            "headers": {
                "Authorization": "Token <tu_token_aqui>"
            }
        },
        "endpoints": {
            "talleres": {
                "url": f"{base_url}talleres-viewset/",
                "metodos": ["GET", "POST", "PUT", "PATCH", "DELETE"],
                "descripcion": "CRUD completo de talleres",
                "filtros": [
                    "?estado=pendiente|aceptado|rechazado",
                    "?categoria=<id_categoria>",
                    "?mis_talleres=true",
                    "?search=<termino_busqueda>",
                    "?ordering=fecha_inicio,-fecha_creacion,nombre,precio"
                ],
                "acciones_especiales": {
                    "mis_talleres": f"{base_url}talleres-viewset/mis_talleres/",
                    "estadisticas": f"{base_url}talleres-viewset/estadisticas/",
                    "proximos": f"{base_url}talleres-viewset/proximos/"
                }
            },
            "recursos": {
                "categorias": f"{base_url}categorias/",
                "lugares": f"{base_url}lugares/",
                "profesores": f"{base_url}profesores/"
            },
            "utilidades": {
                "validar_fecha": f"{base_url}validar-fecha/",
                "documentacion": f"{base_url}docs/"
            }
        },
        "ejemplos": {
            "crear_taller": {
                "url": f"{base_url}talleres-viewset/",
                "metodo": "POST",
                "headers": {
                    "Authorization": "Token <tu_token>",
                    "Content-Type": "application/json"
                },
                "body": {
                    "nombre": "Taller de Fotografía",
                    "descripcion": "Aprende técnicas básicas de fotografía",
                    "categoria": 1,
                    "profesor": 1,
                    "lugar": 1,
                    "fecha_inicio": "2025-08-01",
                    "fecha_fin": "2025-08-30",
                    "hora_inicio": "18:00",
                    "hora_fin": "20:00",
                    "cupos_maximos": 15,
                    "precio": 0
                }
            },
            "listar_talleres": {
                "url": f"{base_url}talleres-viewset/",
                "metodo": "GET",
                "headers": {
                    "Authorization": "Token <tu_token>"
                }
            },
            "obtener_token": {
                "url": request.build_absolute_uri('/api-token-auth/'),
                "metodo": "POST",
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": {
                    "username": "junta",
                    "password": "junta123"
                }
            }
        },
        "codigos_respuesta": {
            "200": "OK - Solicitud exitosa",
            "201": "Created - Recurso creado exitosamente",
            "400": "Bad Request - Error en los datos enviados",
            "401": "Unauthorized - Token inválido o faltante",
            "403": "Forbidden - Sin permisos para esta operación",
            "404": "Not Found - Recurso no encontrado",
            "500": "Internal Server Error - Error del servidor"
        },
        "notas": [
            "Todos los endpoints requieren autenticación con token",
            "Solo usuarios del grupo 'Juntas de Vecinos' pueden acceder",
            "Los talleres se crean con estado 'pendiente' por defecto",
            "Las fechas deben estar en formato YYYY-MM-DD",
            "Las horas deben estar en formato HH:MM",
            "La validación de feriados es automática al crear talleres"
        ]
    }
    
    return Response(documentation)
