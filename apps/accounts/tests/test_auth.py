import pytest 
from django.contrib.auth import get_user_model
from apps.accounts.tests.factories import UserFactory
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@pytest.mark.django_db
class TestRegisterView:

    def test_register_user_success(self, api_client):
        data = {
            "username": "testuser",
            "email": "testuser@gmail.com",
            "first_name": "user",
            "last_name": "test",
            "password": "testuser123"
        }
    
        response = api_client.post('/api/v1/accounts/register/', data, format='json')

        assert response.status_code == 201 

@pytest.mark.django_db
class TestLoginView:

    def test_login_success(self, api_client):
        user = User.objects.create_user(
            username='johndoe',
            email="john@example.com",
            password="Secure123",
        )
        data = {
            'username': 'johndoe',
            "email": "john@example.com",
            "password": "Secure123",
        }
        response = api_client.post("/api/v1/accounts/login/", data, format="json")

        assert response.status_code == 200

@pytest.mark.django_db(transaction=True)
class TestLogoutView:

    def test_logout_success(self, api_client):
        user = UserFactory(is_active=True)
        refresh = RefreshToken.for_user(user)
        api_client.force_authenticate(user=user)
        response = api_client.post('/api/v1/accounts/logout/', {'refresh': str(refresh)}, format='json')

        assert response.status_code == 204 