from django.db import models
from rest_framework import serializers


from posts.models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    created_at = serializers.ReadOnlyField(read_only=True)
    author = serializers.ReadOnlyField(source="author.username")
    # image = serializers.ImageField()
    class Meta:
        model = Post
        fields = ('url', 'pk', 'title', 'slug', 'author', 'body', 'image',
                  'status', 'publish', 'created_at', 'updated_at',)
