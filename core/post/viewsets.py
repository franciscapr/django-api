from rest_framework.permissions import IsAuthenticated

from core.abstract.viewsets import AbstractViewSet
from core.post.models import Post
from core.post.serializers import PostSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


class PostViewSet(AbstractViewSet):
    http_method_names = ('post', 'get')
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