from accounts.api.serializers import UserSerializer
from django.contrib.auth import get_user_model
from posts.api.permissions import IsAuthorOrReadOnly, IsUserOrSuperUserOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
User = get_user_model()


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'


class UserDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'
    permission_classes = [IsUserOrSuperUserOrReadOnly, IsAuthenticatedOrReadOnly]
