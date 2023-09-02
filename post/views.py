"""
Vista para los post de las APIs.
"""
from rest_framework import viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Post
from post import serializers


class PostViewSet(viewsets.ModelViewSet):
    """Vista para la administración de post en las APIs."""
    serializer_class = serializers.PostDetailSerializer
    queryset = Post.objects.all().order_by('-id')
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'date_create']

    def get_query(self):
        """Recuperar posts para el usuario autenticado."""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Retornar la clase de serializador para la solicitud."""
        if self.action == 'list':
            return serializers.PostSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Crear un nuevo post."""
        serializer.save(user=self.request.user)
