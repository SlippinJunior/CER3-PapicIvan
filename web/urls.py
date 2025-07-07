from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('talleres/', views.lista_talleres, name='lista_talleres'),
    path('talleres/<int:taller_id>/', views.detalle_taller, name='detalle_taller'),
]
