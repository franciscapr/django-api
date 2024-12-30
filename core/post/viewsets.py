from rest_framework.permissions import IsAuthenticated

from core.abstract.viewsets import AbstractViewSet
from core.post.models import Post
from core.post.serializers import PostSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action    # Nos permite que los mètodo de la clase ViewSet sean accesibles como rutas.


class PostViewSet(AbstractViewSet):
    http_method_names = ('post', 'get', 'put', 'delete')
    permission_classes = (IsAuthenticated,)
    serializer_class =  PostSerializer


    # Devuelve todas las publicaciones. 
    def get_queryset(self):
        return Post.objects.all()
    
    # Devuelve un objeto de publicaciòn utilizando el public_id que estarà presenta en el URL.
    def get_object(self):
        obj = Post.objects.get_object_by_public_id(self.kwargs['pk'])

        self.check_object_permissions(self.request, obj)

        return obj
    
    # Es la acciòn del viewset que se ejecutra en la solicitud post en el endpoint vinculado al viewset
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)    # Para crear un objeto de publicaciòn.
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)
    

    # detail si se establece en True, la ruta de esta acciòn requerira un identificador especifico del recurso, como un ID.
    # methods, es una lista de mètodos HTTP permitidos por la acciòn
    # *args --> Argumentos posicionales variables "permite que una funciòn reciba un nùmero indefinido de argumentos posicionales"
    # **kwargs --> Es una forma de pasar argumentos nombrados varibles (como pares clave-valor) a una funciòn.


    @action(methods=['post'], detail=True)
    def like(self, request, *args, **kwargs):   
        post = self.get_object()    # Recuperamos el objetos de la publicaciòn
        user = self.request.user
        user.like(post)    # Llamamos la mètodo like del modelo User para marcar la publicaciòn con like.
        serializer = self.serializer_class(post)   # Serializa la publicaciòn actualizada con el contexto de la solicitud y devuelve una respuesta con estado 200 OK
        return Response(serializer.data,    
                        status=status.HTTP_200_OK)
    

    @action(methods=['post'], detail=True)
    def remove_like(self, request, *args, **kwargs):
        post = self.get_object()    # Recuperamos el objetos de la publicaciòn
        user = self.request.user
        user.remove_like(post)    # Llama al mètodo remove_like del modelo User para quitar el like de la publicaciòn.
        serializer = self.serializer_class(post)    # Serializa la publicaciòn actualizada con el contexto de la solicitud y devuelve una respuesta con estado 200 OK
        return Response(serializer.data, status=status.HTTP_200_OK)
