from rest_framework import serializers
from posts.models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    created_at = serializers.ReadOnlyField(read_only=True)
    author = serializers.ReadOnlyField(source="author.username")
    image = serializers.ImageField(max_length=None, allow_empty_file=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ('url', 'pk', 'title', 'slug', 'author', 'body', 'image', 'image_url',
                  'status', 'publish', 'created_at', 'updated_at',)

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None


