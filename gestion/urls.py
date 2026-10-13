from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_gestion, name='gestion_inicio'),

    path('api/libros/', views.api_libros, name='api_libros'),

    path('api/libros/<int:pk>/', views.api_libro, name='api_libro'),

    path('api/autores/', views.api_autores, name='api_autores'),

    path('api/prestamos/', views.api_prestamos, name='api_prestamos'),

    path('api/perfil/', views.api_perfil, name='api_perfil'),

    path('api/estadisticas/', views.api_estadisticas, name='api_estadisticas'),

    path('api/sesion/', views.api_sesion, name='api_sesion'),
]
