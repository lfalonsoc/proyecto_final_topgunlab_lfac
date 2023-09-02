"""
Vista para los comments de las APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Comments
from comments import serializers


class CommentsViewSet(viewsets.ModelViewSet):
    """Vista para la administración de comments en las APIs."""
    serializer_class = serializers.CommentsDetailSerializer
    queryset = Comments.objects.all().order_by('-id')
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_query(self):
        """Recuperar comments para el usuario autenticado."""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Retornar la clase de serializador para la solicitud."""
        if self.action == 'list':
            return serializers.CommentsSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Crear un nuevo comment."""
        serializer.save(user=self.request.user)
