import pytest
from rest_framework import status

from core.fixtures.user import user

# Este mètodo prueba el endopoint de inicio de sesiòn
class TestAuthenticationViewSet:
    
    endpoint = '/api/auth/'

    def test_login(self, client, user):
        data = {
            "username": user.username,
            "password": "test_password"
        }
        response = client.post(self.endpoint + "login/", data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['access']
        assert response.data['user']['id'] == user.public_id.hex
        assert response.data['user']['username'] == user.username
        assert response.data['user']['email'] == user.email
        

# Prueba el mètodo de registro
    @pytest.mark.django_db    
    def test_register(self, client):
        data = {
            "username": "johndoe",
            "email": "johndoe@yopmail.com",
            "password": "test_password",
            "first_name": "John",
            "last_name": "Doe"
        }
        
        response = client.post(self.endpoint + "register/", data)
        assert response.status_code == status.HTTP_201_CREATED


# Prueba el mètodo de actualizaciòn del token
    def test_refresh(self, client, user):
        data = {
            "username": user.username,
            "password": "test_password"
        }
        response = client.post(self.endpoint + "login/", data)

        assert response.status_code == status.HTTP_200_OK
        
        data_refresh = {
            "refresh":  response.data['refresh']
        }
        
        response = client.post(self.endpoint + "refresh/", data_refresh)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['access']




