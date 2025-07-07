#!/bin/bash

# Script de instalación rápida para el Sistema de Talleres Comunitarios
# Municipalidad Villa Verde

echo "🏗️  Instalando Sistema de Talleres Comunitarios - Villa Verde"
echo "=================================================="

# Activar entorno virtual si existe
if [ -d ".venv" ]; then
    echo "📦 Activando entorno virtual..."
    source .venv/bin/activate
else
    echo "❌ Error: No se encontró el entorno virtual .venv"
    echo "Primero ejecuta: python -m venv .venv"
    exit 1
fi

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

# Crear migraciones
echo "🗄️  Creando migraciones..."
python manage.py makemigrations

# Aplicar migraciones
echo "⬆️  Aplicando migraciones..."
python manage.py migrate

# Crear datos iniciales
echo "🌱 Creando datos iniciales..."
python manage.py crear_datos_iniciales

echo ""
echo "✅ ¡Instalación completada exitosamente!"
echo ""
echo "🚀 Para iniciar el servidor ejecuta:"
echo "   python manage.py runserver"
echo ""
echo "🌐 URLs del sistema:"
echo "   - Sitio público: http://localhost:8000/"
echo "   - Admin: http://localhost:8000/admin/"
echo "   - API: http://localhost:8000/api/v1/"
echo ""
echo "👤 Usuarios creados:"
echo "   - admin / admin123 (Administrador)"
echo "   - funcionario / func123 (Funcionario Municipal)"
echo "   - junta / junta123 (Junta de Vecinos)"
echo ""
echo "📚 Revisar README.md para más información."
