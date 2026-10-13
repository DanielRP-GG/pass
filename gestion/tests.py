from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Autor, Libro
from .serializers import LibroSerializer, PrestamoSerializer


class PruebasBiblioteca(APITestCase):

    def setUp(self):
        self.autor = Autor.objects.create(identificacion='A-001', nombre='Gabriel Garcia')
        self.libro = Libro.objects.create(
            titulo='Cien anos de soledad',
            isbn='978-0-00-000001-1',
            categoria='Ficcion',
            precio_alquiler='12.50',
            autor=self.autor,
        )
        self.usuario = User.objects.create_user(
            username='cliente',
            email='cliente@correo.com',
            password='clave12345',
        )
        self.token = Token.objects.create(user=self.usuario)

    def test_serializer_libro_precio_invalido(self):
        datos = {
            'titulo': 'Libro de prueba',
            'isbn': '978-0-00-000002-2',
            'categoria': 'Novela',
            'precio_alquiler': '0',
            'disponible': True,
            'autor': self.autor.id,
        }
        serializer = LibroSerializer(data=datos)
        self.assertFalse(serializer.is_valid())
        self.assertIn('precio_alquiler', serializer.errors)

    def test_serializer_prestamo_costo_negativo(self):
        datos = {
            'libro': self.libro.id,
            'socio_nombre': 'Maria Lopez',
            'dias_prestamo': 5,
            'costo_total': '-50',
        }
        serializer = PrestamoSerializer(data=datos)
        self.assertFalse(serializer.is_valid())
        self.assertIn('costo_total', serializer.errors)

    def test_perfil_anonimo_retorna_401(self):
        respuesta = self.client.get('/gestion/api/perfil/')
        self.assertEqual(respuesta.status_code, 401)

    def test_perfil_autenticado_retorna_200(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        respuesta = self.client.get('/gestion/api/perfil/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.data['id'], self.usuario.id)
        self.assertEqual(respuesta.data['username'], 'cliente')
        self.assertEqual(respuesta.data['email'], 'cliente@correo.com')

    def test_estadisticas_usuario_regular_retorna_403(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        respuesta = self.client.get('/gestion/api/estadisticas/')
        self.assertEqual(respuesta.status_code, 403)

    def test_libros_paginados_con_metadatos(self):
        respuesta = self.client.get('/gestion/api/libros/?page=1')
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.data['total_elementos'], 1)
        self.assertEqual(respuesta.data['total_paginas'], 1)
        self.assertEqual(respuesta.data['pagina_actual'], 1)
        self.assertEqual(len(respuesta.data['datos']), 1)
