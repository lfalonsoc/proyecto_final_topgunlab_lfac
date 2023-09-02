"""
Asignación de URL para la aplicación de comments.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from comments import views


router = DefaultRouter()
router.register('commnents', views.CommentsViewSet)

app_name = 'comments'

urlpatterns = [
    path('', include(router.urls)),
]
