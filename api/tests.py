from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from talleres.models import Taller, Categoria, Lugar, Profesor
from usuarios.models import PerfilUsuario


class TallerAPITestCase(APITestCase):
    """
    Tests para la API de talleres
    """
    
    def setUp(self):
        """
        Configuración inicial para los tests
        """
        # Crear grupos
        self.grupo_jjvv = Group.objects.create(name='Juntas de Vecinos')
        self.grupo_funcionarios = Group.objects.create(name='Funcionarios Municipales')
        
        # Crear usuario junta de vecinos
        self.user_jjvv = User.objects.create_user(
            username='junta_test',
            password='test123',
            email='junta@test.com'
        )
        self.user_jjvv.groups.add(self.grupo_jjvv)
        
        # Crear perfil si no existe
        perfil, created = PerfilUsuario.objects.get_or_create(
            user=self.user_jjvv,
            defaults={
                'tipo_usuario': 'junta_vecinos',
                'nombre_junta': 'Junta Test'
            }
        )
        
        # Crear token
        self.token = Token.objects.create(user=self.user_jjvv)
        
        # Crear datos de prueba
        self.categoria = Categoria.objects.create(
            nombre='Test Categoria',
            descripcion='Categoria para tests'
        )
        
        self.lugar = Lugar.objects.create(
            nombre='Lugar Test',
            direccion='Dirección Test 123',
            capacidad_maxima=50
        )
        
        self.profesor = Profesor.objects.create(
            nombre='Juan',
            apellido='Pérez',
            rut='12345678-9',
            email='profesor@test.com',
            especialidad='Test'
        )
        
        # Configurar cliente API
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    
    def test_listar_talleres(self):
        """
        Test REQ05: Listar todos los talleres
        """
        # Crear taller de prueba
        taller = Taller.objects.create(
            titulo='Taller Test',
            descripcion='Descripción test',
            categoria=self.categoria,
            profesor=self.profesor,
            lugar=self.lugar,
            fecha='2025-08-01',
            hora_inicio='18:00',
            duracion_horas=2.0,
            cupos_maximos=20,
            precio=0,
            creado_por=self.user_jjvv
        )
        
        url = reverse('api:taller-viewset-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['titulo'], 'Taller Test')
    
    def test_crear_taller(self):
        """
        Test REQ04: Crear nuevo taller
        """
        url = reverse('api:taller-viewset-list')
        data = {
            'titulo': 'Nuevo Taller API',
            'descripcion': 'Descripción del nuevo taller',
            'categoria': self.categoria.id,
            'profesor': self.profesor.id,
            'lugar': self.lugar.id,
            'fecha': '2025-08-01',
            'hora_inicio': '18:00',
            'duracion_horas': 2.0,
            'cupos_maximos': 25,
            'precio': 0
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Taller.objects.count(), 1)
        
        taller = Taller.objects.first()
        self.assertEqual(taller.titulo, 'Nuevo Taller API')
        self.assertEqual(taller.estado, 'pendiente')
        self.assertEqual(taller.creado_por, self.user_jjvv)
