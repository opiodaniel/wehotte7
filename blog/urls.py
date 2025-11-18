from rest_framework.routers import DefaultRouter
from .views import PostViewSet, RegisterView
from django.urls import path

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
]

urlpatterns += router.urls
