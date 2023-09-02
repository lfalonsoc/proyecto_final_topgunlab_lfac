"""
Test para post APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
import requests

from core.models import Post

from post.serializers import (
    PostSerializer,
    PostDetailSerializer,
)


POSTS_URL = reverse('post:post-list')


def detail_url(post_id):
    """Crear y retornar una URL de detalle de post."""
    return reverse('post:post-detail', args=[post_id])


def create_post(user, **params):
    """Crear y retornar un post simple"""
    defaults = {
        'title': 'Título post simple',
        'description': 'Descripción simple de post',
        'country_name': 'Colombia',
        'link': 'http://example.com/post.pdf',
    }
    defaults.update(params)

    post = Post.objects.create(user=user, **defaults)
    return post


def create_user(**params):
    """Crear y retornar un nuevo usuario."""
    return get_user_model().objects.create_user(**params)


class PublicPostAPITest(TestCase):
    """Test de solicitud de API no autenticada."""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test autorización requerida para llamar a la API."""
        res = self.client.get(POSTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePostAPITest(TestCase):
    """Test de solicitud de API autenticado."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='testpass123')
        self.client.force_authenticate(self.user)

    def test_retrieve_post(self):
        """Test para recuperar lista de posts."""
        create_post(user=self.user)
        create_post(user=self.user)

        res = self.client.get(POSTS_URL)

        posts = Post.objects.all().order_by('-id')
        serilalizer = PostSerializer(posts, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serilalizer.data)

    # def test_post_list_limited_to_user(self):
    #     """Test lista de posts que esta limitada a usuarios autenticados."""
    #     other_user = create_user(
    #         email='other@ecampĺe.com',
    #         password='password123')
    #     create_post(user=other_user)
    #     create_post(user=self.user)

    #     res = self.client.get(POSTS_URL)

    #     posts = Post.objects.filter(user=self.user)
    #     serializer = PostSerializer(posts, many=True)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)

    def test_get_post_detail(self):
        """Test conseguir detalle de post"""
        post = create_post(user=self.user)

        url = detail_url(post.id)
        res = self.client.get(url)

        serializer = PostDetailSerializer(post)
        self.assertEqual(res.data, serializer.data)

    def test_create_post(self):
        """Test crearando un post."""
        payload = {
            'title': 'Título post simple',
            'country_name': 'Colombia',
        }
        res = self.client.post(POSTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(id=res.data['id'])
        for key, value in payload.items():
            self.assertEqual(getattr(post, key), value)
        self.assertEqual(post.user, self.user)

    def test_partial_update(self):
        """Test actualización parcial de un post"""
        original_link = 'http://example.com/post.pdf'
        post = create_post(
            user=self.user,
            title='Título post simple',
            link=original_link,
        )

        payload = {'title': 'Nuevo título del post'}
        url = detail_url(post.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, payload['title'])
        self.assertEqual(post.link, original_link)
        self.assertEqual(post.user, self.user)

    def test_full_update(self):
        """Test actualización completa del post."""
        post = create_post(
            user=self.user,
            title='Título post simple',
            description='Descripción simple de post',
        )

        payload = {
            'title': 'Nuevo título del post',
            'description': 'Nueva sescripción del post',
            'country_name': 'Japan',
            'link': 'http://example.com/new-post.pdf',
        }
        url = detail_url(post.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        for key, value in payload.items():
            self.assertEqual(getattr(post, key), value)
        self.assertEqual(post.user, self.user)

    def test_update_user_returns_error(self):
        """Test cambiar el usuario del post produce un error."""
        new_user = create_user(email="user2@example.com", password="test123")
        post = create_post(user=self.user)

        payload = {'user': new_user}
        url = detail_url(post.id)
        self.client.patch(url, payload)

        post.refresh_from_db()
        self.assertEqual(post.user, self.user)

    def test_delete_post(self):
        """Test eliminando un post satisfactoriamente."""
        post = create_post(user=self.user)

        url = detail_url(post.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=post.id).exists())

    # def test_delete_other_user_post_error(self):
    #     """Test otro usuario intentando borrar post da error."""
    #     new_user = create_user(email='user2@example.com', password='test123')
    #     post = create_post(user=new_user)

    #     url = detail_url(post.id)
    #     res = self.client.delete(url)

    #     self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertTrue(Post.objects.filter(id=post.id).exists())

    def test_status_code_200(self):
        """Test conexión exitosa con API de paises"""
        res = requests.get('https://restcountries.com/v3.1/all')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # def test_status_code_400(self):
    #     """Test conexión por fallas de solicitud"""
    #     res = requests.get(
    #         'https://restcountries.com/v3.1/all',
    #         headers={'should_error': 'error'},
    #     )

    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_status_code_404(self):
        res = requests.get('https://restcountries.com/v3.1/does_not_exist/')

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
