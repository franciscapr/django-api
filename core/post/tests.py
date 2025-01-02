from django.test import TestCase
import pytest
from core.fixtures.user import user
from core.post.models import Post

# Este archvios se encargarà de probar la creaciòn de un post.

@pytest.mark.django_db
def test_create_post(user):
    post = Post.objects.create(author=user,
                               body="Test Post Body")
    assert post.body == "Test Post Body"
    assert post.author == user



