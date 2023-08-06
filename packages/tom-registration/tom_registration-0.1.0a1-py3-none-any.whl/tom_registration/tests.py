from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import override_settings, TestCase


@override_settings(ROOT_URLCONF='tom_registration.registration_flows.open.urls')
class TestOpenRegistrationViews(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'aaronrodgers',
            'first_name': 'Aaron',
            'last_name': 'Rodgers',
            'email': 'aaronrodgers@berkeley.edu',
            'password1': 'gopackgo',
            'password2': 'gopackgo',
        }

    def test_user_register(self):
        response = self.client.post(reverse('register'), data=self.user_data)
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username=self.user_data['username'])
        self.assertEqual(user.id, auth.get_user(self.client).id)


@override_settings(REGISTRATION_FLOW='APPROVAL_REQUIRED',
                   ROOT_URLCONF='tom_registration.registration_flows.approval_required.urls')
class TestApprovalRegistrationViews(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'aaronrodgers',
            'first_name': 'Aaron',
            'last_name': 'Rodgers',
            'email': 'aaronrodgers@berkeley.edu',
            'password1': 'gopackgo',
            'password2': 'gopackgo',
        }

    def test_user_register(self):
        response = self.client.post(reverse('register'), data=self.user_data)
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username=self.suer_data['username'])
        self.assertFalse(user.is_active)
        self.assertTrue(auth.get_user(self.client).is_anonymous)
