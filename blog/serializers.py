from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    '''

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
        fields = ['id', 'title', 'content', 'owner', 'created_at', 'updated_at']





