from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.abstract.serializers import AbstractSerializer
from core.post.models import Post
from core.user.models import User
from core.user.serializer import UserSerializer


class PostSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(    # Se utiliza para representar el objetivo de la relaciòn utilizando un compo en el objetivo.
        queryset=User.objects.all(), slug_field='public_id'
    )

    def validate_author(self, value):
        if self.context["request"].user != value:
            raise ValidationError("You can`t create a post for another user.")
        return value
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = User.objects.get_object_by_public_id["author"]
        rep["author"] = UserSerializer(author).data

        return rep



    class Meta:
        model = Post
        # List of all the fileds that can be included in a request or a response
        fields = ['id', 'author', 'body', 'edited', 'created', 'updated']
        read_only_fields = ["edited"]