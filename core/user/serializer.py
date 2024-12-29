from core.user.models import User
from core.abstract.serializers import AbstractSerializer

class UserSerializer(AbstractSerializer):
    class Meta:
        model = User
        # Lista de todos los campos que se pueden incluir en una solicitud o respuesta
        fields = ['id', 'username', 'first_name', 'last_name', 'bio', 'avatar',
                  'email',
                  'is_active', 'created', 'updated']
        # Lista de todos los campos que solo pueden ser leídos por el usuario
        read_only_field = ['is_active']

    