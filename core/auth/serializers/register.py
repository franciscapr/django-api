from rest_framework import serializers

from core.user.serializer import UserSerializer
from core.user.models import User

class RegisterSerializer(UserSerializer):
    """Registration serializer for requests and user creation"""
    # Asegurándose de que la contraseña tenga al menos 8 caracteres de longitud, no más de 128, y que no pueda ser leída
    # por el usuario
    password = serializers.CharField(max_length=128,
                                     min_length=8, write_only=True, required=True)
    
    class Meta:
         model = User
         # Lista de todos los campos que pueden incluirse en una solicitud o respuesta
         fields = ['id', 'bio', 'avatar', 'email', 'username', 'first_name', 'last_name', 'password']

    # class Meta:
    #     model = User
    #     # Lista de todos los campos que pueden incluirse en una solicitud o respuesta
    #     fields = ['id', 'email', 'username', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        # Usa el método 'create_user' que escribimos anteriormente para el UserManager para crear un nuevo usuario.
        return User.objects.create_user(**validated_data)