from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Autor, Libro, Prestamo
from .serializers import AutorSerializer, LibroSerializer, PrestamoSerializer


class PaginacionLibros(PageNumberPagination):
    page_size = 5

    def get_paginated_response(self, data):
        return Response({
            "total_elementos": self.page.paginator.count,
            "total_paginas": self.page.paginator.num_pages,
            "pagina_actual": self.page.number,
            "datos": data,
        })


@api_view(['GET'])
def api_gestion(request):
    return Response({
        "Respuesta": "API de Gestion de Biblioteca activa"
    })


@api_view(['GET', 'POST'])
def api_libros(request):
    if request.method == 'GET':
        libros = Libro.objects.all().order_by('titulo')

        categoria = request.query_params.get('categoria')
        if categoria:
            libros = libros.filter(categoria__iexact=categoria)

        disponible = request.query_params.get('disponible')
        if disponible is not None:
            libros = libros.filter(disponible=disponible.lower() == 'true')

        autor_id = request.query_params.get('autor_id')
        if autor_id:
            if not autor_id.isdigit():
                return Response({
                    'error': 'autor_id debe ser un numero entero'
                }, status=status.HTTP_400_BAD_REQUEST)
            libros = libros.filter(autor_id=int(autor_id))

        paginador = PaginacionLibros()
        pagina = paginador.paginate_queryset(libros, request)
        serializer = LibroSerializer(pagina, many=True)
        return paginador.get_paginated_response(serializer.data)

    serializer = LibroSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_libro(request, pk):
    try:
        libro = Libro.objects.get(pk=pk)
    except Libro.DoesNotExist:
        return Response({
            'error': 'Libro no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LibroSerializer(libro)
        return Response(serializer.data)

    if request.method in ['PUT', 'PATCH']:
        serializer = LibroSerializer(libro, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        libro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def api_autores(request):
    if request.method == 'GET':
        autores = Autor.objects.all().order_by('nombre')
        serializer = AutorSerializer(autores, many=True)
        return Response(serializer.data)

    serializer = AutorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def api_prestamos(request):
    if request.method == 'GET':
        prestamos = Prestamo.objects.all().order_by('fecha_prestamo')
        serializer = PrestamoSerializer(prestamos, many=True)
        return Response(serializer.data)

    serializer = PrestamoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_perfil(request):
    return Response({
        "id": request.user.id,
        "username": request.user.username,
        "email": request.user.email,
    })


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def api_estadisticas(request):
    return Response({
        "total_autores": Autor.objects.count(),
        "total_libros": Libro.objects.count(),
        "libros_disponibles": Libro.objects.filter(disponible=True).count(),
        "total_prestamos": Prestamo.objects.count(),
    })


@api_view(['GET'])
def api_sesion(request):
    accesos = request.session.get('accesos', 0) + 1
    request.session['accesos'] = accesos
    return Response({
        "accesos": accesos
    })
