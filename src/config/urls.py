"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from posts.api import views as posts_views
from accounts.api import views as accounts_views
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework.generics import GenericAPIView


class ApiRoot(GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'posts': reverse(posts_views.PostListAPIView.name, request=request),
            'users': reverse(accounts_views.UserListAPIView.name, request=request),
        })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ApiRoot.as_view(), name=ApiRoot.name),
    path('posts/', include('posts.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('accounts.api.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
