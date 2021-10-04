from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView


from posts.api.serializers import PostSerializer
from posts.models import Post

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from posts.api.permissions import IsAuthorOrReadOnly


class PostListAPIView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    name = 'post-list'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

from rest_framework.parsers import FileUploadParser, MultiPartParser

class PostDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    name = 'post-detail'
    permission_classes = [IsAuthorOrReadOnly]
    # parser_classes = (FileUploadParser, )

    # def patch(self, request, pk=None, *args, **kwargs):
    #     context = {'request': request}
    #     print(self.get_object())
    #     print('patch request')
    #     post_serializer = PostSerializer(instance=self.get_object(), data=request.data, partial=True, context=context)
    #     print(post_serializer)
    #     if post_serializer.is_valid():
    #         post_serializer.save()
    #         print('saving....')
    #         return Response(post_serializer.data, status=status.HTTP_200_OK)
    #     return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
