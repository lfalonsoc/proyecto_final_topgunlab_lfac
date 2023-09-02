"""
Serializers para los post de las APIs.
"""
from rest_framework import serializers

from core.models import Post


class PostSerializer(serializers.ModelSerializer):
    """Serializer para los posts."""

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'country_name',
                  'link', 'date_create', 'date_modify']
        read_only_fields = ['id', 'user', 'date_create', 'date_modify']


class PostDetailSerializer(PostSerializer):
    """Serializer para la vista detallada de posts."""

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ['description']
