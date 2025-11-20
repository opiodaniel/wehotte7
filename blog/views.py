
from .models import Post, Comment, PostLike, CommentLike
from .serializers import PostSerializer
from rest_framework import generics
from .serializers import RegisterSerializer, CommentSerializer
from django.contrib.auth import get_user_model
from .permissions import IsOwnerOrReadOnly
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

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

    @action(detail=True, methods=['get', 'post'], url_path="comments")
    def comments(self, request, pk=None):
        post = self.get_object()

        if request.method == "GET":
            comments = post.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

        if request.method == "POST":
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(
                    post=post,
                    author=request.user
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        # Check if user already liked the post
        liked = PostLike.objects.filter(post=post, user=user).first()

        if liked:
            # Unlike
            liked.delete()
            return Response({"message": "Unliked"}, status=status.HTTP_200_OK)

        # Like
        PostLike.objects.create(post=post, user=user)
        return Response({"message": "Liked"}, status=status.HTTP_201_CREATED)        
           



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


    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        comment = self.get_object()
        user = request.user

        # Check if user already liked the comment
        liked = CommentLike.objects.filter(comment=comment, user=user).first()

        if liked:
            # Unlike
            liked.delete()
            return Response({"message": "Unliked"}, status=status.HTTP_200_OK)

        # Like
        CommentLike.objects.create(comment=comment, user=user)
        return Response({"message": "Liked"}, status=status.HTTP_201_CREATED)            
