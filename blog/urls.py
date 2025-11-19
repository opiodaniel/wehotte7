from rest_framework.routers import DefaultRouter
from .views import PostViewSet, RegisterView, CommentViewSet
from django.urls import path

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts'),
router.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
]

urlpatterns += router.urls
