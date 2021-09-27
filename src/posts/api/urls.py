from django.urls import path


from .import views

urlpatterns = [
    path('', views.PostListAPIView.as_view(), name=views.PostListAPIView.name),
    path('<int:pk>/', views.PostDetailAPIView.as_view(),
         name=views.PostDetailAPIView.name),

]
