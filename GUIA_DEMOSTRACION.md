# Guía de Demostración - Certamen Talleres Comunitarios Villa Verde

## 📋 Resumen Ejecutivo

Este documento detalla **cómo demostrar cada requerimiento** del certamen de manera clara y convincente. Incluye scripts de demostración, datos específicos y secuencias paso a paso.

## 🎯 Estrategia de Presentación

### Orden Recomendado de Demostración:
1. **Vista general del sistema** (2 min)
2. **REQ01**: Frontend público con filtros (3 min)
3. **REQ02 + REQ07**: Administración y gestión de usuarios (4 min)
4. **REQ03**: Cambio de estados de talleres (2 min)
5. **REQ06**: Validación automática de feriados (3 min)
6. **REQ04 + REQ05**: API completa para Juntas de Vecinos (4 min)
7. **REQ08**: Demostración de restricciones de visibilidad (2 min)

**Tiempo total estimado: 20 minutos**

---

## 🚀 Preparación Previa

### 1. Iniciar el Sistema
```bash
cd /home/papic/Documents/USM/TLP/Certamen3
.venv/bin/python manage.py runserver
```

### 2. URLs a Tener Abiertas en Pestañas
- Frontend: http://localhost:8000/
- Admin: http://localhost:8000/admin/
- Postman/Thunder Client preparado para API

### 3. Credenciales Preparadas
```
Admin: admin / admin123 (superusuario - acceso total)
Funcionario: funcionario / func123 (staff con permisos específicos REQ02)
Junta 5: junta5 / junta123 (API)
Junta 12: junta12 / junta123 (API)
```

---

## 📊 Demostración Detallada por Requerimiento

### REQ01: Listado Público de Talleres con Filtros
**🎯 Objetivo:** Mostrar que el público puede ver talleres aceptados con filtros

**📍 URL:** http://localhost:8000/talleres/

**🎬 Script de Demostración:**

1. **Abrir la página principal**
   ```
   → Mostrar: "Aquí está el frontend público del sistema"
   → Navegar a: Lista de Talleres
   ```

2. **Demostrar filtros por categoría**
   ```
   → Explicar: "Solo se muestran talleres aceptados y futuros"
   → Filtrar por: "Aire Libre" → mostrar talleres específicos
   → Filtrar por: "Arte" → mostrar cambio de resultados
   → Quitar filtro → mostrar todos los talleres
   ```

3. **Mostrar información completa**
   ```
   → Hacer clic en un taller específico
   → Mostrar: fecha, hora, lugar, profesor, descripción
   → Explicar: "Toda la información relevante está disponible"
   ```

**💬 Puntos Clave a Mencionar:**
- "Solo talleres ACEPTADOS son visibles al público"
- "Solo talleres FUTUROS aparecen"
- "Filtros funcionan dinámicamente"
- "Interfaz responsive para móviles"

---

### REQ02: Gestión desde Django Admin
**🎯 Objetivo:** Demostrar la gestión completa desde el panel administrativo

**📍 URL:** http://localhost:8000/admin/

**🎬 Script de Demostración:**

1. **Login como Funcionario Municipal (REQ02)**
   ```
   Usuario: funcionario
   Contraseña: func123
   → Mostrar: "Funcionarios municipales tienen acceso específico"
   → Explicar: "NO es superusuario, solo permisos específicos"
   ```

2. **Mostrar gestión de Lugares**
   ```
   → Ir a: Talleres → Lugares
   → Mostrar: 10 lugares precargados (según anexos)
   → Demostrar: Agregar nuevo lugar
   → Campos: nombre, dirección, capacidad máxima
   → Guardar y mostrar en lista
   → Explicar: "Funcionario puede crear/modificar/eliminar lugares"
   ```

3. **Mostrar gestión de Categorías**
   ```
   → Ir a: Talleres → Categorías
   → Mostrar: 10 categorías exactas de los anexos
   → Demostrar: Editar una categoría existente
   → Explicar: "Funcionario puede gestionar categorías"
   ```

4. **Mostrar gestión de Profesores**
   ```
   → Ir a: Talleres → Profesores
   → Mostrar: Profesores con especialidades
   → Demostrar: Crear nuevo profesor
   → Mostrar: Campo de especialidad, nombre, apellido
   → Explicar: "Funcionario puede gestionar profesores"
   ```

5. **Mostrar gestión de Usuarios JJVV**
   ```
   → Ir a: Usuarios → Perfiles de usuario
   → Mostrar: perfiles existentes de juntas
   → Demostrar: Crear nuevo usuario JJVV
   → Ir a: Autenticación → Usuarios
   → Mostrar: puede crear/editar usuarios
   → Explicar: "Funcionario puede gestionar usuarios de Juntas de Vecinos"
   ```

**💬 Puntos Clave a Mencionar:**
- "Funcionario NO es admin, tiene permisos limitados y específicos"
- "Puede gestionar exactamente lo requerido: lugares, categorías, profesores, usuarios JJVV"
- "Sistema de permisos granular implementado"
- "Cumple REQ02: gestión completa desde Django Admin"

---

### REQ07: Sistema de Roles y Permisos
**🎯 Objetivo:** Mostrar diferentes tipos de usuario y sus roles específicos

**🎬 Script de Demostración:**

1. **Demostrar diferencias entre usuarios (ya logueado como funcionario)**
   ```
   → Explicar roles mientras navegas:
     * Admin (admin): acceso total (superusuario)
     * Funcionario (funcionario): gestión específica según REQ02
     * Junta: solo API para proponer talleres
   ```

2. **Mostrar grupos automáticos**
   ```
   → Ir a: Autenticación y autorización → Grupos
   → Mostrar: "Funcionarios Municipales" con permisos específicos
   → Mostrar: "Juntas de Vecinos" para acceso a API
   → Explicar: "Asignación automática según tipo de usuario"
   ```

3. **Demostrar limitaciones del funcionario**
   ```
   → Mostrar que funcionario NO puede:
     * Acceder a configuración del sitio
     * Gestionar otros superusuarios
     * Cambiar configuraciones críticas
   → Explicar: "Permisos granulares según rol"
   ```

**💬 Puntos Clave:**
- "Sistema de roles específico para cada tipo de usuario"
- "Funcionarios tienen exactamente los permisos del REQ02"
- "Juntas solo pueden usar la API"
- "Seguridad por capas implementada"

---

### REQ03: Cambio de Estado de Talleres
**🎯 Objetivo:** Demostrar gestión de estados y flujo de aprobación

**📍 Desde:** Django Admin → Talleres → Talleres

**🎬 Script de Demostración:**

1. **Mostrar talleres con diferentes estados**
   ```
   → Filtrar por estado: "Pendiente"
   → Mostrar: talleres esperando aprobación
   → Filtrar por estado: "Aceptado"
   → Mostrar: talleres aprobados
   ```

2. **Cambiar estado de un taller**
   ```
   → Seleccionar un taller "Pendiente"
   → Cambiar estado a: "Aceptado"
   → Guardar
   → Explicar: "Ahora será visible en el frontend público"
   ```

3. **Demostrar rechazo con observaciones**
   ```
   → Seleccionar otro taller
   → Cambiar a: "Rechazado"
   → Agregar observación: "Fecha no disponible"
   → Guardar
   → Mostrar: no aparece en frontend
   ```

**💬 Puntos Clave:**
- "Control total del flujo de aprobación"
- "Observaciones para comunicar decisiones"
- "Estados reflejados inmediatamente en público"

---

### REQ06: Validación Automática de Feriados
**🎯 Objetivo:** Demostrar integración con API de feriados de Chile

**🎬 Script de Demostración:**

1. **Mostrar talleres existentes rechazados automáticamente**
   ```
   → En Admin, ir a Talleres → Talleres
   → Filtrar por estado: "Rechazado"
   → Mostrar talleres del 18 de septiembre (Independencia)
   → Explicar: "Rechazados automáticamente por estar en feriado irrenunciable"
   → Mostrar observación: "No se programan talleres en feriados irrenunciables"
   ```

2. **Crear taller en feriado irrenunciable para demostrar**
   ```
   → En Admin, crear nuevo taller
   → Fecha de inicio: 2025-09-18 (Independencia)
   → Categoría: cualquiera excepto "Aire Libre"
   → Guardar
   → Mostrar: Estado automático "Rechazado"
   → Observación: "No se programan talleres en feriados irrenunciables"
   ```

3. **Demostrar desde API REST**
   ```
   → Usar script: python test_api_feriados.py
   → Mostrar: talleres en feriados se rechazan automáticamente
   → Mostrar: API devuelve estado y observación en respuesta
   ```

4. **Crear taller de Aire Libre en feriado no irrenunciable**
   ```
   → Crear taller con categoría "Aire Libre"
   → Fecha: feriado no irrenunciable (ej. 2025-06-29, San Pedro y San Pablo)
   → Guardar
   → Mostrar: Estado "Pendiente" (permitido)
   ```

5. **Mostrar servicio funcionando**
   ```
   → Ir a: Externos → Feriado Caches
   → Mostrar: feriados consultados y cached
   → Explicar: "Sistema consulta API oficial automáticamente"
   → Mencionar: "Fallback con feriados hardcodeados para garantizar funcionamiento"
   ```

**📅 Feriados Útiles para Demostración (2025-2026):**

| Fecha | Feriado | Tipo | Resultado Esperado |
|-------|---------|------|-------------------|
| 2025-09-18 | Día de las Glorias del Ejército | Irrenunciable | Rechazado automáticamente |
| 2025-11-01 | Día de Todos los Santos | Irrenunciable | Rechazado automáticamente |
| 2025-12-25 | Navidad | Irrenunciable | Rechazado automáticamente |
| 2025-06-29 | San Pedro y San Pablo | No irrenunciable | Pendiente (Aire Libre permitido) |
| 2025-05-21 | Día de las Glorias Navales | No irrenunciable | Pendiente (Aire Libre permitido) |
| 2026-01-01 | Año Nuevo | Irrenunciable | Rechazado automáticamente |

💡 **Tip para la demostración:** Usar 18 de septiembre es ideal porque es un feriado muy conocido.

---

### REQ04: API para Proponer Talleres
**🎯 Objetivo:** Demostrar que Juntas de Vecinos pueden proponer talleres via API

**🛠️ Herramienta:** Postman, Thunder Client, o curl

**🎬 Script de Demostración:**

1. **Obtener token de autenticación**
   ```http
   POST http://localhost:8000/api-token-auth/
   Content-Type: application/json

   {
     "username": "junta5",
     "password": "junta123"
   }

   token:"53bddf9f13516dde0d623b07eb98abafe999a23f"

   → Mostrar respuesta con token
   → Explicar: "Cada junta tiene credenciales únicas"
   ```

2. **Consultar recursos disponibles**
   ```http
   GET http://localhost:8000/api/v1/categorias/
   Headers: Authorization: Token 53bddf9f13516dde0d623b07eb98abafe999a23f

   → Demostrar en Postman:
     1. Método GET
     2. URL: categorias/
     3. Headers → Add → Key: Authorization, Value: Token [pegar-token]
     4. Send → Mostrar 10 categorías según anexos
   
   → Repetir para:
     - /api/v1/lugares/ → 10 lugares
     - /api/v1/profesores/ → 5 profesores
   
   → Explicar: "Junta consulta recursos antes de proponer taller"
   ```

3. **Proponer nuevo taller**
   ```http
   POST http://localhost:8000/api/v1/talleres-viewset/
   Authorization: Token [token-obtenido]
   Content-Type: application/json

   {
     "titulo": "Taller de Huerto Comunitario",
     "descripcion": "Aprende a cultivar vegetales en espacios pequeños",
     "categoria": 8,
     "profesor": 101,
     "lugar": 1,
     "fecha": "2025-08-15",
     "hora_inicio": "15:00",
     "duracion_horas": 2,
     "cupos_maximos": 25,
     "precio": 0
   }

   → Usar IDs correctos:
     * categoria: 8 (Medioambiente - ideal para huerto)
     * profesor: 101 (Carolina Rivas)
     * lugar: 1 (Jardín Botánico - perfecto para huerto)
   
   → Mostrar: Taller creado con estado "pendiente"
   → Ir a Admin y mostrar el nuevo taller
   ```

4. **Demostrar validación de feriados irrenunciables (REQ06)**
   ```http
   POST http://localhost:8000/api/v1/talleres-viewset/
   Authorization: Token [token-obtenido]
   Content-Type: application/json

   {
     "titulo": "Taller de Fotografía Urbana",
     "descripcion": "Aprende técnicas de fotografía en espacios urbanos",
     "categoria": 2,
     "profesor": 102,
     "lugar": 4,
     "fecha": "2025-09-18",
     "hora_inicio": "10:00",
     "duracion_horas": 3,
     "cupos_maximos": 15,
     "precio": 0
   }

   → Explicar: "18 de septiembre es feriado irrenunciable (Independencia)"
   → Mostrar respuesta: Taller creado pero estado "rechazado"
   → Mostrar observación automática: "No se programan talleres en feriados irrenunciables"
   → Ir a Admin y verificar: estado rechazado automáticamente
   
   → Puntos clave:
     * API consulta feriados en tiempo real
     * Validación automática sin intervención manual
     * Integración real con API gubernamental chilena
   ```

**💬 Puntos Clave:**
- "API completa para Juntas de Vecinos"
- "Validaciones automáticas en tiempo real"
- "Integración directa con sistema administrativo"
- "REQ06: Validación automática de feriados funcionando en la API"
- "Sistema rechaza automáticamente talleres en feriados irrenunciables"

---

### REQ05: API para Ver Todos los Talleres
**🎯 Objetivo:** Mostrar que Juntas ven TODOS los talleres (no solo públicos)

**🎬 Script de Demostración:**

1. **Consultar todos los talleres**
   ```http
   GET http://localhost:8000/api/v1/talleres-viewset/
   Authorization: Token [token-junta5]

   → Mostrar respuesta completa
   → Contar talleres mostrados
   ```

2. **Comparar con frontend público**
   ```
   → Abrir http://localhost:8000/talleres/
   → Contar talleres visibles
   → Explicar: "API muestra MÁS talleres que el público"
   → Explicar: "Incluye pendientes, rechazados, pasados"
   ```

3. **Mostrar información completa**
   ```
   → En respuesta JSON mostrar:
     * Estado de cada taller
     * Información de creador (propuesto_por)
     * Fechas de creación/modificación
     * Observaciones administrativas
   ```

**💬 Puntos Clave:**
- "Acceso privilegiado para Juntas de Vecinos"
- "Transparencia total del proceso"
- "Información administrativa incluida"

---

### REQ08: Restricción de Visibilidad
**🎯 Objetivo:** Demostrar que solo talleres aceptados y futuros son públicos

**🎬 Script de Demostración:**

1. **Mostrar taller rechazado en Admin**
   ```
   → En Admin: buscar taller con estado "Rechazado"
   → Mostrar: fecha, estado, observaciones
   → Copiar nombre del taller
   ```

2. **Verificar invisibilidad en frontend**
   ```
   → Ir a frontend público
   → Buscar el taller rechazado → NO aparece
   → Explicar: "Solo aceptados son visibles"
   ```

3. **Mostrar taller pasado**
   ```
   → En Admin: crear taller con fecha pasada
   → Estado: "Aceptado"
   → Guardar
   → Ir a frontend → NO aparece
   → Explicar: "Solo talleres futuros son visibles"
   ```

4. **Demostrar visibilidad correcta**
   ```
   → Cambiar taller a fecha futura
   → Estado: "Aceptado"
   → Guardar
   → Ir a frontend → SÍ aparece
   → Explicar: "Ahora cumple ambas condiciones"
   ```

---

## 🎬 Script de Demostración Completa (20 min)

### Introducción (2 min)
```
"Buenos días. Voy a demostrar el Sistema de Talleres Comunitarios 
desarrollado para la Municipalidad de Villa Verde. Este sistema 
cumple 100% con los requerimientos del certamen y está basado 
en Django con API REST."

→ Mostrar arquitectura en pantalla
→ Mencionar datos exactos de anexos precargados
```

### Demo Frontend (3 min)
```
"Comenzamos con la vista pública donde ciudadanos consultan talleres"

→ REQ01: Demostrar filtros y navegación
→ Enfatizar: solo talleres aceptados y futuros
```

### Demo Administración (6 min)
```
"Ahora el panel administrativo donde funcionarios municipales 
gestionan todo el sistema"

→ REQ02: Gestión de lugares, categorías, profesores
→ REQ07: Gestión de usuarios y roles
→ REQ03: Cambio de estados con observaciones
```

### Demo Validación Feriados (3 min)
```
"Una característica única: validación automática contra 
feriados chilenos oficiales"

→ REQ06: Crear talleres en feriados
→ Mostrar rechazo automático
→ Mostrar excepción para "Aire Libre"
```

### Demo API Completa (4 min)
```
"La API permite a Juntas de Vecinos proponer talleres 
y consultar el estado completo"

→ REQ04: Proponer taller via API
→ REQ05: Ver todos los talleres (incluye estados)
→ Mostrar documentación automática
```

### Demo Restricciones (2 min)
```
"Para finalizar, el sistema de restricciones que garantiza 
que solo información apropiada es pública"

→ REQ08: Comparar visibilidad Admin vs Frontend
→ Demostrar filtrado automático
```

---

## 🏆 Puntos de Diferenciación a Destacar

### 1. **Exactitud de Anexos**
- "Todos los datos están exactamente según anexos oficiales"
- "10 categorías, 10 lugares, 5 profesores específicos"

### 2. **Integración Real**
- "API de feriados de Chile oficial funcionando"
- "No es simulación, es integración real"

### 3. **Robustez Técnica**
- "Validaciones automáticas en múltiples niveles"
- "Cache inteligente para optimización"
- "Tests automatizados pasando"

### 4. **Usabilidad Completa**
- "Sistema listo para producción"
- "Documentación técnica completa"
- "Datos de prueba incluidos"

### 5. **Extensibilidad**
- "Arquitectura preparada para nuevas funcionalidades"
- "API versionada para compatibilidad futura"

---

## 📝 Checklist de Verificación Final

Antes de la presentación, verificar:

- [ ] ✅ Servidor Django corriendo sin errores
- [ ] ✅ Base de datos poblada con datos de anexos
- [ ] ✅ Usuario admin funciona (admin/admin123)
- [ ] ✅ Usuarios junta5/junta12 funcionan
- [ ] ✅ Frontend muestra talleres aceptados
- [ ] ✅ API responde correctamente
- [ ] ✅ Validación de feriados activa
- [ ] ✅ Documentación accesible
- [ ] ✅ Postman/Thunder Client configurado
- [ ] ✅ URLs importantes en favoritos

---

## 🎯 Mensajes Clave para Cerrar

1. **"Este sistema cumple 100% los requerimientos del certamen"**
2. **"Está listo para producción en una municipalidad real"**
3. **"Incluye características únicas como validación automática de feriados"**
4. **"La documentación técnica permite mantener y expandir el sistema"**
5. **"Es un ejemplo de desarrollo Django profesional y completo"**

---

## 📞 Soporte para Preguntas

### Preguntas Técnicas Comunes:

**P: "¿Cómo se asegura la seguridad de la API?"**
R: "Autenticación por token, verificación de grupos, validaciones múltiples"

**P: "¿Qué pasa si la API de feriados no funciona?"**
R: "Cache local mantiene funcionamiento, solo nuevas consultas fallan gracefully"

**P: "¿Se puede agregar más funcionalidad?"**
R: "Sí, arquitectura modular permite extensiones sin modificar código existente"

**P: "¿Funciona en móviles?"**
R: "Frontend completamente responsive con Bootstrap"

---

**¡Tu sistema está listo para impresionar! 🚀**
