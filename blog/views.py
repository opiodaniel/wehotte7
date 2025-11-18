from rest_framework import viewsets, permissions
from .models import Post
from .serializers import PostSerializer
from rest_framework import generics
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    # Automatically attach the logged-in user as owner
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []   # Anyone can register

 