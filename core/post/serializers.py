from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.abstract.serializers import AbstractSerializer
from core.post.models import Post
from core.user.models import User
from core.user.serializer import UserSerializer


class PostSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(    # Se utiliza para representar el objetivo de la relaciòn utilizando un compo en el objetivo.
        queryset=User.objects.all(), slug_field='public_id')    # Utilizamos public_id para recuperar al usuario
    liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    # Este mètodo verifica si el usuario que realiza la solicitud ya ha dado like a la publicaciòn. Accede al usuario de la solicitud y verifica si existe una relaciòn entre el usuario y al publicaciòn en la tabla posts_liked.
    def get_liked(self, instance):
        request = self.context.get('request', None)

        if request is None or request.user.is_anonymous:
            return False
        
        return request.user.has_liked(instance)
    
    # Este mètodo devuelve el conteo total de usuario que han dado like a la publicaciòn, utilizando el campo liked_by que hemos añadido al modelo Post.
    def get_likes_count(self, instance):
        return instance.liked_by.count()


    def validate_author(self, value):
        if self.context["request"].user != value:
            raise ValidationError("You can`t create a post for another user.")
        return value
    
    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data['edited'] = True

        instance = super().update(instance, validated_data)
        return instance
    

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = User.objects.get_object_by_public_id(rep["author"])
        rep["author"] = UserSerializer(author).data

        return rep

    class Meta:
        model = Post
        # List of all the fileds that can be included in a request or a response
        fields = ['id', 'author', 'body', 'edited', 'liked', 'likes_count', 'created', 'updated']
        read_only_fields = ["edited"]