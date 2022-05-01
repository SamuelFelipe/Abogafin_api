from re import I
from webbrowser import get
from django.test import TestCase
from django.contrib.auth import get_user_model
from lawyers.models import Lawyer
from django.db import IntegrityError


class LawyerTests(TestCase):

    User = get_user_model()

    def test_create_lawyer(self):
        user = self.User.objects.create_user(email='generic@user.com', password='foo')
        lawyer = Lawyer.objects.create(user=user, profesional_card='10', webpage='user.com', linked_in='linkedin.com')
        self.assertEqual(lawyer.user, user)
        self.assertEqual(lawyer.profesional_card, '10')
        self.assertEqual(lawyer.webpage, 'user.com')
        self.assertEqual(lawyer.linked_in, 'linkedin.com')

    def test_invalid_user(self):
        with self.assertRaises(IntegrityError):
            Lawyer.objects.create(user=None)
