
from .models import Post, Comment
from .serializers import PostSerializer
from rest_framework import generics
from .serializers import RegisterSerializer, CommentSerializer
from django.contrib.auth import get_user_model
from .permissions import IsOwnerOrReadOnly
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Exact filtering
    filterset_fields = ['title', 'owner__username']

    # Keyword search
    search_fields = ['title', 'content', 'owner__username']

    # Sorting
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    # Automatically attach the logged-in user as owner
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)        



User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []   # Anyone can register

 
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['post', 'author__username']
    search_fields = ['content', 'author__username']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
