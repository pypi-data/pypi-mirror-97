# -*- coding: utf-8 -*-

import datetime

from hashlib import sha1
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from django.core import mail

from tcms.auth.models import UserActivateKey
from tests import AuthMixin

# ### Test cases for models ###


class TestSetRandomKey(TestCase):
    """Test case for UserActivateKey.set_random_key_for_user"""

    @classmethod
    def setUpTestData(cls):
        cls.new_user = User.objects.create(username='new-tester',
                                           email='new-tester@example.com',
                                           password='password')

    @patch('tcms.auth.models.datetime')
    @patch('tcms.auth.models.random')
    def test_set_random_key(self, random, mock_datetime):
        mock_datetime.datetime.today.return_value = datetime.datetime(2017, 5, 10)
        mock_datetime.timedelta.return_value = datetime.timedelta(7)
        fake_random = 0.12345678
        random.random.return_value = fake_random

        activation_key = UserActivateKey.set_random_key_for_user(self.new_user)

        self.assertEqual(self.new_user, activation_key.user)

        s_random = sha1(str(fake_random).encode('utf-8')).hexdigest()[:5]
        expected_key = sha1('{}{}'.format(
            s_random, self.new_user.username).encode('utf-8')).hexdigest()

        self.assertEqual(expected_key, activation_key.activation_key)
        self.assertEqual(datetime.datetime(2017, 5, 17),
                         activation_key.key_expires)


class TestForceToSetRandomKey(TestCase):
    """Test case for UserActivateKey.set_random_key_for_user forcely"""

    @classmethod
    def setUpTestData(cls):
        cls.new_user = User.objects.create(username='new-tester',
                                           email='new-tester@example.com',
                                           password='password')
        cls.origin_activation_key = UserActivateKey.set_random_key_for_user(cls.new_user)

    def test_set_random_key_forcely(self):
        new_activation_key = UserActivateKey.set_random_key_for_user(self.new_user,
                                                                     force=True)
        self.assertEqual(self.origin_activation_key.user, new_activation_key.user)
        self.assertNotEqual(self.origin_activation_key.activation_key,
                            new_activation_key.activation_key)


# ### Test cases for view methods ###

class TestLogout(AuthMixin, TestCase):
    """Test for logout view method"""

    auto_login = True

    def test_logout_then_redirect_to_next(self):
        response = self.client.get(reverse('nitrate-logout'), follow=True)
        self.assertRedirects(response, reverse('nitrate-login'))

    def test_logout_then_goto_next(self):
        next_url = reverse('plans-all')
        response = self.client.get(
            reverse('nitrate-logout'), {'next': next_url}, follow=True)
        self.assertRedirects(response, next_url)


class TestRegistration(TestCase):

    def setUp(self):
        self.register_url = reverse('nitrate-register')
        self.fake_activate_key = 'secret-activate-key'

    def test_open_registration_page(self):
        response = self.client.get(self.register_url)
        self.assertContains(
            response,
            '<input value="Register" class="loginbutton sprites" type="submit">',
            html=True)

    @patch('tcms.auth.models.sha1')
    def assert_user_registration(self, username, sha1):
        sha1.return_value.hexdigest.return_value = self.fake_activate_key

        response = self.client.post(self.register_url,
                                    {'username': username,
                                     'password1': 'password',
                                     'password2': 'password',
                                     'email': 'new-tester@example.com'})
        self.assertContains(
            response,
            '<a href="{}">Continue</a>'.format(reverse('nitrate-index')),
            html=True)

        users = User.objects.filter(username=username)
        self.assertTrue(users.exists())

        user = users[0]
        self.assertEqual('new-tester@example.com', user.email)
        self.assertFalse(user.is_active)

        keys = UserActivateKey.objects.filter(user=user)
        self.assertTrue(keys.exists())
        self.assertEqual(self.fake_activate_key, keys[0].activation_key)

        return response

    @patch('tcms.auth.views.settings.EMAIL_HOST', new='smtp.example.com')
    def test_register_user_by_email_confirmation(self):
        response = self.assert_user_registration('new-tester')

        self.assertContains(
            response,
            'Your account has been created, please check your mailbox for confirmation')

        # Verify notification mail
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(settings.EMAIL_FROM, mail.outbox[0].from_email)
        self.assertIn(reverse('nitrate-activation-confirm',
                              args=[self.fake_activate_key]),
                      mail.outbox[0].body)

    @patch('tcms.auth.views.settings.EMAIL_HOST', new='')
    @patch('tcms.auth.views.settings.ADMINS',
           new=[('admin1', 'admin1@example.com'),
                ('admin2', 'admin2@example.com')])
    def test_register_user_and_activate_by_admin(self):
        response = self.assert_user_registration('plan-tester')

        self.assertContains(
            response,
            'Your account has been created, but you need to contact an administrator '
            'to active your account')

        self.assertContains(
            response,
            '<ul><li><a href="mailto:{}">{}</a></li>'
            '<li><a href="mailto:{}">{}</a></li></ul>'.format(
                'admin1@example.com', 'admin1',
                'admin2@example.com', 'admin2'),
            html=True)


class TestConfirm(TestCase):
    """Test for activation key confirmation"""

    @classmethod
    def setUpTestData(cls):
        cls.new_user = User.objects.create(username='new-user',
                                           email='new-user@example.com',
                                           password='password')

    def test_fail_if_activation_key_not_exist(self):
        confirm_url = reverse('nitrate-activation-confirm',
                              args=['nonexisting-activation-key'])
        response = self.client.get(confirm_url)

        self.assertContains(
            response,
            'This key no longer exist in the database')

        self.assertContains(
            response,
            '<a href="{}">Continue</a>'.format(reverse('nitrate-index')),
            html=True)

    def test_confirm(self):
        fake_activate_key = 'secret-activate-key'

        with patch('tcms.auth.models.sha1') as sha1:
            sha1.return_value.hexdigest.return_value = fake_activate_key
            UserActivateKey.set_random_key_for_user(self.new_user)

        confirm_url = reverse('nitrate-activation-confirm',
                              args=[fake_activate_key])
        response = self.client.get(confirm_url)

        self.assertContains(
            response,
            'Your account has been activated successfully')

        self.assertContains(
            response,
            '<a href="{}">Continue</a>'.format(
                reverse('user-profile-redirect')),
            html=True)

        user = User.objects.get(username=self.new_user.username)
        self.assertTrue(user.is_active)
        activate_key_deleted = not UserActivateKey.objects.filter(user=user).exists()
        self.assertTrue(activate_key_deleted)
