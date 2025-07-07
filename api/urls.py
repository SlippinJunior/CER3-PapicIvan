from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .docs import api_documentation

app_name = 'api'

# Router para ViewSets
router = DefaultRouter()
router.register(r'talleres-viewset', views.TallerViewSet, basename='taller-viewset')

urlpatterns = [
    # Documentación de la API
    path('docs/', api_documentation, name='api-docs'),
    
    # ViewSet routes (nueva implementación)
    path('', include(router.urls)),
    
    # Endpoints originales (mantener compatibilidad)
    path('talleres/', views.TallerListCreateView.as_view(), name='taller-list-create'),
    path('talleres/<int:pk>/', views.TallerDetailView.as_view(), name='taller-detail'),
    
    # Recursos auxiliares
    path('categorias/', views.categorias_list, name='categorias-list'),
    path('lugares/', views.lugares_list, name='lugares-list'),
    path('profesores/', views.profesores_list, name='profesores-list'),
    
    # Utilidades
    path('validar-fecha/', views.validar_fecha_feriado, name='validar-fecha'),
]
