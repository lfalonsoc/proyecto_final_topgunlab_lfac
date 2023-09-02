"""
Serializers para los comments de las APIs.
"""
from rest_framework import serializers

from core.models import Comments


class CommentsSerializer(serializers.ModelSerializer):
    """Serializer para los comments."""

    class Meta:
        model = Comments
        fields = ['id', 'user', 'post', 'date_create', 'date_modify']
        read_only_fields = ['id', 'user', 'date_create', 'date_modify']


class CommentsDetailSerializer(CommentsSerializer):
    """Serializer para la vista detallada de comments."""

    class Meta(CommentsSerializer.Meta):
        fields = CommentsSerializer.Meta.fields + ['comment']
