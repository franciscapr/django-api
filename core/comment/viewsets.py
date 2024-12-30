from django.http.response import Http404
from rest_framework.response import Response
from rest_framework import status

from core.abstract.viewsets import AbstractViewSet
from core.comment.models import Comment
from core.comment.serializers import CommentSerializer
from core.auth.permissions import UserPermission

class CommentViewSet(AbstractViewSet):
    http_method_names = ('post', 'get', 'put', 'delete')
    permission_classes = (UserPermission,)
    serializer_class = CommentSerializer

    # Llamamos al mètodo cuando el usuario accede a /api/post/post_pk/comment/
    def get_queryset(self):
        if self.request.user.is_superuser:  # Comprobamos si el usuario es superusuario
            return Comment.objects.all()    # Si es el caso, se devuelven todos los objetos de comentarios en la base de datos.
        
        post_pk = self.kwargs['post_pk']    # SI el usuario no es superusuario, entonces se devuelven los comentarios relacionados con una publicaciòn.
        if post_pk is None:
            return Http404
        queryset = Comment.objects.filter(
            post__public_id=post_pk
        )
        return queryset
    
    # Este mètodo se llama en cada solicitud realizada al endpoint /api/post/post_pk/comment/comment_pk/
    def get_object(self):
        obj = Comment.objects.get_object_by_public_id(
            self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer.data, status=status.HTTP_201_CREATED)