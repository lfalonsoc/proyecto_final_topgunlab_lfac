"""
Database models.
"""
from django.conf import settings

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Administrador de usuarios."""

    def create_user(self, email, password=None, **extra_fields):
        """Crear, salvar y retornar un nuevo usuario."""
        if not email:
            raise ValueError('El usuario debe tener una dirección de email.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Crear y retornar un nuevo superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Usuario en el sistema."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Post(models.Model):
    """Objeto post."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    country_name = models.CharField(max_length=100)
    link = models.CharField(max_length=255, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_modify = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Comments(models.Model):
    """Objeto comentarios."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='users',
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_modify = models.DateTimeField(auto_now=True)

    class Meta():
        ordering = ('date_create',)

    def __str__(self) -> str:
        return f'Comentario del {self.post}'
