from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class AuthTests(APITestCase):
    def test_register_login_refresh_logout(self):
        reg_url = reverse('users:register')
        login_url = reverse('users:token_obtain_pair')
        refresh_url = reverse('users:token_refresh')
        logout_url = reverse('users:logout')
        me_url = reverse('users:me')

        data = {
            "username": "akram",
            "email": "akram@example.com",
            "password": "Str0ngPassw0rd!",
            "password2": "Str0ngPassw0rd!",
        }

        # Register
        r = self.client.post(reg_url, data, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        # Login
        r = self.client.post(login_url, {"username": "akram", "password": "Str0ngPassw0rd!"}, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertIn('access', r.data)
        self.assertIn('refresh', r.data)
        refresh = r.data['refresh']
        access = r.data['access']

        # Get current user
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        r = self.client.get(me_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['username'], 'akram')

        # Refresh token
        r = self.client.post(refresh_url, {"refresh": refresh}, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertIn('access', r.data)

        # Logout (blacklist refresh)
      #  r = self.client.post(logout_url, {"refresh": refresh}, format='json')
       # self.assertEqual(r.status_code, status.HTTP_205_RESET_CONTENT)
