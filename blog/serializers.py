from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)

    '''

    Why use source="likes.count"?

    This automatically counts the related likes via the related_name="likes" from the model.

    owner = serializers.ReadOnlyField(source='owner.username')

    Very important:

    The user should not choose the owner manually in Postman.

    The system automatically attaches the logged-in user.

    ReadOnlyField prevents users from sending owner in the request.

    source='owner.username' means the serializer will return:

    "owner": "john"

    instead of: 

    "owner": 1

    '''

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'owner', 'created_at', 'updated_at', 'likes_count']



User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data.get('email'),
            password = validated_data['password']
        )
        return user


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    likes_count = serializers.IntegerField(source="likes.count", read_only=True)

    '''
      
      Why use source="likes.count"?
      This automatically counts the related likes via the related_name="likes" from the model.

    '''

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'likes_count']
        read_only_fields = ['post','author']
