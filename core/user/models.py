import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404
from core.abstract.models import AbstractModel, AbstractManager

class UserManager(BaseUserManager, AbstractManager):
        
    def create_user(self, username, email, password=None, **kwargs):
        """Create and return a 'USER' whit an emai, phone numbrer, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must hace an email.')
        if password is None:
            raise TypeError('User must hace an email.')
        
        user = self.model(username=username, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, username, email, password, **kwargs):
        """Create and return a 'USER' with superuser (admin) permissions."""
        if password is None:
            raise TypeError('Superusers must have a password.')
        if email is None:
            raise TypeError('Superusers must hace an email.')
        if username is None:
            raise TypeError('Superusers must have an username.')
        
        user = self.create_user(user, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user




class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True)
    posts_liked = models.ManyToManyField(
        "core_post.Post",
        related_name="liked_by"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'
    
    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'
    

    # Mètodo utilizados para dar like a una publicaciòn. Para esto utilizaremos el mètodo add() de los models, y ManyToManyField para vincular un apublicaciòn a un usuario.
    def like(self, post):
        """Like 'post' if it hasn`t been done yet"""
        return self.posts_liked.add(post)
    
    
    # Se utiliza para quitar like de una publicaciòn. Pra esto, usaremos el mètodo remove() de los modelos. Utilizaremos ManyToManyFiedl para desvincular una publicaciòn de una usuario.
    def remove_like(self, post):
        """Remove a like from a 'post'"""
        return self.posts_liked.remove(post)
    

    # Se utiliz para devolver True si el usuario ha dado Like a un publicaciòn; de lo contrario, False.
    def has_liked(self, post):
        """ Return True if theuser has liked a 'post'; else False"""
        return self.posts_liked.filter(pk=post.pk).exists()
    
