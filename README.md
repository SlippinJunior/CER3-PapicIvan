# Sistema de Talleres Comunitarios - Municipalidad Villa Verde

**Certamen 3 - Taller de Lenguaje de Programación**  
**USM - Ingeniería en Informática**

## 🏗️ Arquitectura del Sistema

### Aplicaciones Django

1. **`talleres`** - Core: gestión de talleres, categorías, lugares y profesores
2. **`usuarios`** - Sistema de roles y autenticación extendido
3. **`web`** - Frontend público para consulta de talleres (REQ01, REQ08)
4. **`api`** - API REST completa para Juntas de Vecinos (REQ04, REQ05)
5. **`externos`** - Integración con API de feriados de Chile (REQ06)

### Modelos Principales

#### App `talleres`
- `Categoria` - Categorías de talleres
- `Lugar` - Lugares donde se realizan talleres
- `Profesor` - Instructores de los talleres
- `Taller` - Modelo principal con estados y validaciones

#### App `usuarios`
- `PerfilUsuario` - Extensión del modelo User con roles específicos

#### App `externos`
- `FeriadoCache` - Cache local de feriados para optimización

## Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- pip

### Pasos de Instalación

1. **Clonar y configurar el entorno virtual**
```bash
cd /home/papic/Documents/USM/TLP/Certamen3
python -m venv .venv
source .venv/bin/activate  # En Linux/Mac
# .venv\Scripts\activate  # En Windows
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar la base de datos**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Crear datos iniciales**
```bash
python manage.py crear_datos_iniciales
```

5. **Ejecutar el servidor**
```bash
python manage.py runserver
```

## Acceso al Sistema

### URLs Principales
- **Sitio Web Público**: http://localhost:8000/
- **Lista de Talleres**: http://localhost:8000/talleres/
- **Panel de Administración**: http://localhost:8000/admin/
- **API para Juntas de Vecinos**: http://localhost:8000/api/v1/

### Usuarios Predefinidos

El comando `crear_datos_iniciales` crea los siguientes usuarios:

| Usuario | Contraseña | Rol | Acceso |
|---------|------------|-----|--------|
| admin | admin123 | Administrador | Django Admin completo |
| funcionario | func123 | Funcionario Municipal | Django Admin (gestión) |
| junta | junta123 | Junta de Vecinos | Solo API |

## API Endpoints (Juntas de Vecinos)

### Autenticación
La API utiliza autenticación por token y sesión. Los usuarios deben pertenecer al grupo "Juntas de Vecinos".

### Endpoints Principales

#### ViewSet de Talleres (Recomendado)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/talleres-viewset/` | Listar todos los talleres (REQ05) |
| POST | `/api/v1/talleres-viewset/` | Proponer nuevo taller (REQ04) |
| GET | `/api/v1/talleres-viewset/{id}/` | Detalle de un taller |
| PUT/PATCH | `/api/v1/talleres-viewset/{id}/` | Actualizar taller |
| DELETE | `/api/v1/talleres-viewset/{id}/` | Eliminar taller |

#### Acciones Especiales del ViewSet

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/talleres-viewset/mis_talleres/` | Talleres del usuario actual |
| GET | `/api/v1/talleres-viewset/estadisticas/` | Estadísticas de talleres |
| GET | `/api/v1/talleres-viewset/proximos/` | Talleres próximos (aceptados y futuros) |

#### Recursos Auxiliares

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/categorias/` | Listar categorías disponibles |
| GET | `/api/v1/lugares/` | Listar lugares disponibles |
| GET | `/api/v1/profesores/` | Listar profesores disponibles |

#### Utilidades

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/validar-fecha/` | Validar fecha contra feriados |
| GET | `/api/v1/docs/` | Documentación interactiva de la API |

### Filtros y Búsqueda

La API soporta múltiples filtros y opciones de búsqueda:

#### Filtros por Query Parameters
- `?estado=pendiente|aceptado|rechazado` - Filtrar por estado
- `?categoria=<id>` - Filtrar por categoría
- `?mis_talleres=true` - Solo talleres del usuario actual
- `?search=<término>` - Búsqueda en nombre, descripción, categoría, profesor
- `?ordering=fecha_inicio,-fecha_creacion,nombre,precio` - Ordenamiento

#### Ejemplos de Filtros
```bash
# Talleres pendientes de mi junta de vecinos
GET /api/v1/talleres-viewset/?estado=pendiente&mis_talleres=true

# Buscar talleres de yoga
GET /api/v1/talleres-viewset/?search=yoga

# Talleres ordenados por fecha de inicio
GET /api/v1/talleres-viewset/?ordering=fecha_inicio
```

### Ejemplo de Uso API

**Obtener token de autenticación:**
```bash
curl -X POST http://localhost:8000/api-token-auth/ \
     -H "Content-Type: application/json" \
     -d '{"username": "junta", "password": "junta123"}'
```

**Listar talleres:**
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
     http://localhost:8000/api/v1/talleres-viewset/
```

**Proponer nuevo taller:**
```bash
curl -X POST http://localhost:8000/api/v1/talleres-viewset/ \
     -H "Authorization: Token YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "nombre": "Nuevo Taller",
       "descripcion": "Descripción del taller",
       "categoria": 1,
       "profesor": 1,
       "lugar": 1,
       "fecha_inicio": "2025-08-01",
       "fecha_fin": "2025-08-30",
       "hora_inicio": "18:00",
       "hora_fin": "20:00",
       "cupos_maximos": 25,
       "precio": 0
     }'
```

**Ver mis talleres:**
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
     http://localhost:8000/api/v1/talleres-viewset/mis_talleres/
```

**Obtener estadísticas:**
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
     http://localhost:8000/api/v1/talleres-viewset/estadisticas/
```

## Funcionalidades Especiales

### Validación de Feriados (REQ06)
El sistema consulta automáticamente la API oficial de feriados de Chile:
- Si la fecha es **feriado irrenunciable**: Taller rechazado automáticamente
- Si la fecha es **feriado no irrenunciable**: Solo permite talleres "Aire Libre"
- Cache local para optimizar consultas repetidas

### Sistema de Roles
- **Administradores**: Acceso completo al sistema
- **Funcionarios Municipales**: Gestión de talleres, lugares, categorías y profesores
- **Juntas de Vecinos**: Solo acceso a API para proponer y consultar talleres

### Estados de Talleres
- **Pendiente**: Talleres recién creados (por defecto)
- **Aceptado**: Talleres aprobados y visibles públicamente
- **Rechazado**: Talleres no aprobados (por feriados u otras razones)