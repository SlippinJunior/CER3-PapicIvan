from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from talleres.models import Taller, Categoria


def lista_talleres(request):
    """
    Vista pública para mostrar talleres (REQ01, REQ08)
    Solo muestra talleres aceptados y con fecha futura
    """
    # Obtener talleres visibles públicamente
    talleres = Taller.objects.filter(
        estado='aceptado',
        fecha__gte=timezone.now().date()
    ).select_related('categoria', 'profesor', 'lugar').order_by('fecha')
    
    # Filtro por categoría
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        talleres = talleres.filter(categoria_id=categoria_id)
    
    # Paginación
    paginator = Paginator(talleres, 12)  # 12 talleres por página
    page_number = request.GET.get('page')
    talleres_page = paginator.get_page(page_number)
    
    # Obtener categorías para el filtro
    categorias = Categoria.objects.filter(activa=True).order_by('nombre')
    
    context = {
        'talleres': talleres_page,
        'categorias': categorias,
        'categoria_seleccionada': categoria_id,
    }
    
    return render(request, 'web/lista_talleres.html', context)


def detalle_taller(request, taller_id):
    """
    Vista para mostrar el detalle de un taller público
    """
    taller = get_object_or_404(
        Taller.objects.select_related('categoria', 'profesor', 'lugar'),
        id=taller_id,
        estado='aceptado',
        fecha__gte=timezone.now().date()
    )
    
    context = {
        'taller': taller,
    }
    
    return render(request, 'web/detalle_taller.html', context)


def inicio(request):
    """
    Página de inicio del sitio web
    """
    # Próximos talleres destacados
    talleres_destacados = Taller.objects.filter(
        estado='aceptado',
        fecha__gte=timezone.now().date()
    ).select_related('categoria', 'profesor', 'lugar').order_by('fecha')[:6]
    
    # Estadísticas básicas
    total_talleres = Taller.objects.filter(
        estado='aceptado',
        fecha__gte=timezone.now().date()
    ).count()
    
    categorias_disponibles = Categoria.objects.filter(
        activa=True,
        taller__estado='aceptado',
        taller__fecha__gte=timezone.now().date()
    ).distinct().count()
    
    context = {
        'talleres_destacados': talleres_destacados,
        'total_talleres': total_talleres,
        'categorias_disponibles': categorias_disponibles,
    }
    
    return render(request, 'web/inicio.html', context)
