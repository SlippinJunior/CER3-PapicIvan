"""
Script para crear datos iniciales del sistema
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.utils import timezone
from datetime import date, time, timedelta
from talleres.models import Categoria, Lugar, Profesor, Taller
from usuarios.models import PerfilUsuario


class Command(BaseCommand):
    help = 'Crea datos iniciales para el sistema de talleres'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creando datos iniciales...'))
        
        # Crear grupos
        self._crear_grupos()
        
        # Crear usuarios
        admin_user = self._crear_usuarios()
        
        # Crear categorías
        self._crear_categorias()
        
        # Crear lugares
        self._crear_lugares()
        
        # Crear profesores
        self._crear_profesores()
        
        # Crear talleres de ejemplo
        self._crear_talleres(admin_user)
        
        self.stdout.write(
            self.style.SUCCESS('Datos iniciales creados exitosamente!')
        )
        
        self.stdout.write(
            self.style.WARNING('\nCredenciales de acceso:')
        )
        self.stdout.write('Administrador: admin / admin123')
        self.stdout.write('Funcionario: funcionario / func123')
        self.stdout.write('Junta de Vecinos: junta / junta123')

    def _crear_grupos(self):
        grupos = [
            'Administradores',
            'Funcionarios Municipales', 
            'Juntas de Vecinos'
        ]
        
        for nombre_grupo in grupos:
            grupo, created = Group.objects.get_or_create(name=nombre_grupo)
            if created:
                self.stdout.write(f'Grupo creado: {nombre_grupo}')

    def _crear_usuarios(self):
        # Usuario administrador
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@villaverde.cl',
                'first_name': 'Administrador',
                'last_name': 'Sistema',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            perfil, _ = PerfilUsuario.objects.get_or_create(
                user=admin_user,
                defaults={'tipo_usuario': 'administrador'}
            )
            self.stdout.write('Usuario administrador creado')
        
        # Usuario funcionario
        funcionario_user, created = User.objects.get_or_create(
            username='funcionario',
            defaults={
                'email': 'funcionario@villaverde.cl',
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'is_staff': True
            }
        )
        if created:
            funcionario_user.set_password('func123')
            funcionario_user.save()
            perfil, _ = PerfilUsuario.objects.get_or_create(
                user=funcionario_user,
                defaults={'tipo_usuario': 'funcionario'}
            )
            self.stdout.write('Usuario funcionario creado')
        
        # Usuario junta de vecinos
        junta_user, created = User.objects.get_or_create(
            username='junta',
            defaults={
                'email': 'junta@villaverde.cl',
                'first_name': 'María',
                'last_name': 'González'
            }
        )
        if created:
            junta_user.set_password('junta123')
            junta_user.save()
            perfil, _ = PerfilUsuario.objects.get_or_create(
                user=junta_user,
                defaults={
                    'tipo_usuario': 'junta_vecinos',
                    'nombre_junta': 'Junta de Vecinos Villa Verde Norte',
                    'sector': 'Norte'
                }
            )
            self.stdout.write('Usuario junta de vecinos creado')
        
        return admin_user

    def _crear_categorias(self):
        categorias = [
            ('Aire Libre', 'Actividades recreativas y deportivas al aire libre'),
            ('Arte y Cultura', 'Talleres de expresión artística y cultural'),
            ('Deportes', 'Actividades físicas y deportivas'),
            ('Educación', 'Talleres educativos y de capacitación'),
            ('Tecnología', 'Talleres de informática y tecnología'),
            ('Salud y Bienestar', 'Actividades para el bienestar físico y mental')
        ]
        
        for nombre, descripcion in categorias:
            categoria, created = Categoria.objects.get_or_create(
                nombre=nombre,
                defaults={'descripcion': descripcion}
            )
            if created:
                self.stdout.write(f'Categoría creada: {nombre}')

    def _crear_lugares(self):
        lugares = [
            ('Centro Comunitario Norte', 'Av. Principal 123', 50),
            ('Gimnasio Municipal', 'Calle Deportes 456', 80),
            ('Sala de Computación', 'Av. Tecnología 789', 25),
            ('Plaza Central', 'Plaza Villa Verde', 100),
            ('Biblioteca Municipal', 'Calle Cultura 321', 30),
            ('Cancha de Fútbol', 'Complejo Deportivo Municipal', 200)
        ]
        
        for nombre, direccion, capacidad in lugares:
            lugar, created = Lugar.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'direccion': direccion,
                    'capacidad_maxima': capacidad
                }
            )
            if created:
                self.stdout.write(f'Lugar creado: {nombre}')

    def _crear_profesores(self):
        profesores = [
            ('Ana', 'Martínez', '12345678-9', 'ana.martinez@email.com', 'Yoga y Pilates'),
            ('Carlos', 'Rodríguez', '87654321-0', 'carlos.rodriguez@email.com', 'Fútbol y Deportes'),
            ('Laura', 'Silva', '11223344-5', 'laura.silva@email.com', 'Arte y Pintura'),
            ('Pedro', 'González', '55667788-1', 'pedro.gonzalez@email.com', 'Informática'),
            ('Carmen', 'López', '99887766-K', 'carmen.lopez@email.com', 'Cocina Saludable'),
            ('Roberto', 'Morales', '44556677-2', 'roberto.morales@email.com', 'Guitarra y Música')
        ]
        
        for nombre, apellido, rut, email, especialidad in profesores:
            profesor, created = Profesor.objects.get_or_create(
                rut=rut,
                defaults={
                    'nombre': nombre,
                    'apellido': apellido,
                    'email': email,
                    'especialidad': especialidad
                }
            )
            if created:
                self.stdout.write(f'Profesor creado: {nombre} {apellido}')

    def _crear_talleres(self, admin_user):
        # Obtener datos necesarios
        categorias = {cat.nombre: cat for cat in Categoria.objects.all()}
        lugares = {lugar.nombre: lugar for lugar in Lugar.objects.all()}
        profesores = list(Profesor.objects.all())
        
        # Talleres de ejemplo
        talleres = [
            {
                'nombre': 'Yoga para Principiantes',
                'descripcion': 'Aprende los fundamentos del yoga en un ambiente relajado y acogedor.',
                'categoria': categorias.get('Salud y Bienestar'),
                'profesor': profesores[0],
                'lugar': lugares.get('Centro Comunitario Norte'),
                'fecha_inicio': date.today() + timedelta(days=10),
                'fecha_fin': date.today() + timedelta(days=40),
                'hora_inicio': time(18, 0),
                'hora_fin': time(19, 30),
                'cupos_maximos': 20,
                'estado': 'aceptado'
            },
            {
                'nombre': 'Fútbol Juvenil',
                'descripcion': 'Taller de fútbol para jóvenes entre 12 y 18 años.',
                'categoria': categorias.get('Deportes'),
                'profesor': profesores[1],
                'lugar': lugares.get('Cancha de Fútbol'),
                'fecha_inicio': date.today() + timedelta(days=7),
                'fecha_fin': date.today() + timedelta(days=35),
                'hora_inicio': time(16, 0),
                'hora_fin': time(17, 30),
                'cupos_maximos': 30,
                'estado': 'aceptado'
            },
            {
                'nombre': 'Pintura al Óleo',
                'descripcion': 'Técnicas básicas y avanzadas de pintura al óleo.',
                'categoria': categorias.get('Arte y Cultura'),
                'profesor': profesores[2],
                'lugar': lugares.get('Centro Comunitario Norte'),
                'fecha_inicio': date.today() + timedelta(days=15),
                'fecha_fin': date.today() + timedelta(days=50),
                'hora_inicio': time(19, 0),
                'hora_fin': time(21, 0),
                'cupos_maximos': 15,
                'estado': 'aceptado'
            },
            {
                'nombre': 'Computación Básica',
                'descripcion': 'Aprende a usar computadoras, internet y aplicaciones básicas.',
                'categoria': categorias.get('Tecnología'),
                'profesor': profesores[3],
                'lugar': lugares.get('Sala de Computación'),
                'fecha_inicio': date.today() + timedelta(days=5),
                'fecha_fin': date.today() + timedelta(days=30),
                'hora_inicio': time(14, 0),
                'hora_fin': time(16, 0),
                'cupos_maximos': 20,
                'estado': 'aceptado'
            },
            {
                'nombre': 'Taller de Guitarra',
                'descripcion': 'Aprende a tocar guitarra desde cero.',
                'categoria': categorias.get('Arte y Cultura'),
                'profesor': profesores[5],
                'lugar': lugares.get('Biblioteca Municipal'),
                'fecha_inicio': date.today() + timedelta(days=20),
                'fecha_fin': date.today() + timedelta(days=60),
                'hora_inicio': time(18, 30),
                'hora_fin': time(20, 0),
                'cupos_maximos': 12,
                'estado': 'pendiente'
            }
        ]
        
        for taller_data in talleres:
            if taller_data['categoria'] and taller_data['lugar']:
                taller, created = Taller.objects.get_or_create(
                    nombre=taller_data['nombre'],
                    defaults={
                        **taller_data,
                        'propuesto_por': admin_user
                    }
                )
                if created:
                    self.stdout.write(f'Taller creado: {taller_data["nombre"]}')
