from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from core.abstract.serializers import AbstractSerializer
from core.post.models import Post
from core.user.models import User


class PostSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(    # Se utiliza para representar el objetivo de la relaciòn utilizando un compo en el objetivo.
        queryset=User.objects.all(), slug_field='public_id'
    )

    def validate_author(self, value):
        if self.context["request"].user != value:
            raise ValidationError("You can`t create a post for another user.")
        return value
    
    class Meta:
        model = Post
        # List of all the fileds that can be included in a request or a response
        fields = ['id', 'author', 'body', 'edited', 'created', 'updated']
        read_only_fields = ["edited"]