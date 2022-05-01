from random import randint
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.forms import ValidationError
from django.test import TestCase

from califications.models import LawFirmCalification, UserCalification
from lawfirms.models import LawFirm


class UserCalificationTests(TestCase):

    User = get_user_model()
    content = 'lorem ipsum dolor sit amet'

    def setUp(self):
        self.main_user = self.User.objects.create_user(email='mainuser@sample.com', password='foo')
        return super().setUp()

    def test_cal_creation(self):
        u1 = self.User.objects.create_user(email='user1@sample.com', password='foo')
        UserCalification.objects.create(owner=u1, target=self.main_user, content=self.content, score=5)
        self.assertEqual(UserCalification.objects.filter(target=self.main_user).count(), 1)

    def test_replicated_cal_creation(self):
        u1 = self.User.objects.create_user(email='user1@sample.com', password='foo')
        UserCalification.objects.create(owner=u1, target=self.main_user, content=self.content, score=5)
        with transaction.atomic():
            with self.assertRaises(ValidationError):
                UserCalification.objects.create(owner=u1, target=self.main_user, content=self.content, score=1)
        cal = UserCalification.objects.create(owner=self.main_user, target=u1, content=self.content, score=3.5)
        self.assertIsInstance(cal, UserCalification)
        self.assertEqual(UserCalification.objects.filter(owner=self.main_user).count(), 1)

    def test_califications_delete(self):
        u1 = self.User.objects.create_user(email='user1@sample.com', password='foo')
        cal = UserCalification.objects.create(owner=u1, target=self.main_user, content=self.content, score=5)
        self.assertEqual(UserCalification.objects.filter(owner=u1).count(), 1)
        cal.delete()
        self.assertEqual(UserCalification.objects.filter(owner=u1).count(), 0)

    def test_calification_cascade_delete(self):
        u1 = self.User.objects.create_user(email='user1@sample.com', password='foo')
        u2 = self.User.objects.create_user(email='user2@sample.com', password='foo')
        UserCalification.objects.create(owner=u1, target=u2, content=self.content, score=5)
        UserCalification.objects.create(owner=self.main_user, target=u2, content=self.content, score=5)
        UserCalification.objects.create(owner=self.main_user, target=u1, content=self.content, score=5)
        UserCalification.objects.create(owner=u2, target=u1, score=5, content=self.content)
        self.assertEqual(UserCalification.objects.filter(target=u2).count(), 2)
        self.assertEqual(UserCalification.objects.filter(owner=u2).count(), 1)
        self.assertEqual(UserCalification.objects.all().count(), 4)
        u2.delete()
        self.assertEqual(UserCalification.objects.all().count(), 1)

    def test_avoid_autocalification(self):
        with self.assertRaises(ValidationError):
            UserCalification.objects.create(owner=self.main_user, target=self.main_user, content=self.content, score=5)

    def test_invalid_score_error(self):
        u1 = self.User.objects.create_user(email='user1@sample.com', password='foo')
        with transaction.atomic():
            with self.assertRaises(ValidationError):
                UserCalification.objects.create(owner=u1, target=self.main_user, content=self.content, score=-1)
        with transaction.atomic():
            with self.assertRaises(ValidationError):
                UserCalification.objects.create(owner=u1, target=self.main_user, content=self.content, score=6)

    def test_empty_short_message_error(self):
        u1 = self.User.objects.create_user(email='user1@sample.com', password='foo')
        with transaction.atomic():
            with self.assertRaises(ValidationError):
                UserCalification.objects.create(owner=u1, target=self.main_user, content='', score=1)
        with transaction.atomic():
            with self.assertRaises(ValidationError):
                UserCalification.objects.create(owner=u1, target=self.main_user, content='Hi!', score=5)


class LawFirmCalificationTests(TestCase):

    User = get_user_model()
    content = 'lorem ipsum dolor sit ammet'

    def setUp(self):
        self.main_lf = LawFirm.objects.create(name='hi', nit='100')
        return super().setUp()

    def test_cal_creation(self):
        u1 = self.User.objects.create_user(email='user1@sample.com', password='foo')
        LawFirmCalification.objects.create(owner=u1, target=self.main_lf, content=self.content, score=5)
        self.assertEqual(LawFirmCalification.objects.filter(target=self.main_lf).count(), 1)

    def test_replicated_cal_creation(self):
        u1 = self.User.objects.create_user(email='user1@sample.com', password='foo')
        LawFirmCalification.objects.create(owner=u1, target=self.main_lf, content=self.content, score=5)
        with transaction.atomic():
            with self.assertRaises(ValidationError):
                LawFirmCalification.objects.create(owner=u1, target=self.main_lf, content=self.content, score=1)
        self.assertEqual(LawFirmCalification.objects.filter(owner=u1).count(), 1)

    def test_califications_delete(self):
        u1 = self.User.objects.create_user(email='user1@sample.com', password='foo')
        cal = LawFirmCalification.objects.create(owner=u1, target=self.main_lf, content=self.content, score=5)
        self.assertEqual(LawFirmCalification.objects.filter(owner=u1).count(), 1)
        cal.delete()
        self.assertEqual(LawFirmCalification.objects.filter(owner=u1).count(), 0)
        self.assertEqual(LawFirmCalification.objects.filter(target=self.main_lf).count(), 0)

    def test_calification_cascade_delete_user(self):
        u1 = self.User.objects.create_user(email='user1@sample.com', password='foo')
        u2 = self.User.objects.create_user(email='user2@sample.com', password='foo')
        LawFirmCalification.objects.create(target=self.main_lf, owner=u2, content=self.content, score=5)
        LawFirmCalification.objects.create(target=self.main_lf, owner=u1, content=self.content, score=5)
        self.assertEqual(LawFirmCalification.objects.filter(target=self.main_lf).count(), 2)
        self.assertEqual(LawFirmCalification.objects.filter(owner=u2).count(), 1)
        self.assertEqual(LawFirmCalification.objects.all().count(), 2)
        u2.delete()
        self.assertEqual(LawFirmCalification.objects.all().count(), 1)
    
    def test_calification_cascade_delete_lawfirm(self):
        u1 = self.User.objects.create_user(email='user1@sample.com', password='foo')
        u2 = self.User.objects.create_user(email='user2@sample.com', password='foo')
        LawFirmCalification.objects.create(target=self.main_lf, owner=u2, content=self.content, score=5)
        LawFirmCalification.objects.create(target=self.main_lf, owner=u1, content=self.content, score=5)
        self.assertEqual(LawFirmCalification.objects.filter(target=self.main_lf).count(), 2)
        self.assertEqual(LawFirmCalification.objects.filter(owner=u2).count(), 1)
        self.assertEqual(LawFirmCalification.objects.all().count(), 2)
        self.main_lf.delete()
        self.assertEqual(LawFirmCalification.objects.all().count(), 0)

    def test_invalid_score_error(self):
        u1 = self.User.objects.create_user(email='user1@sample.com', password='foo')
        with transaction.atomic():
            with self.assertRaises(ValidationError):
                LawFirmCalification.objects.create(owner=u1, target=self.main_lf, content=self.content, score=-1)
        with transaction.atomic():
            with self.assertRaises(ValidationError):
                LawFirmCalification.objects.create(owner=u1, target=self.main_lf, content=self.content, score=6)

    def test_empty_message_error(self):
        u1 = self.User.objects.create_user(email='user1@sample.com', password='foo')
        with transaction.atomic():
            with self.assertRaises(ValidationError):
                LawFirmCalification.objects.create(owner=u1, target=self.main_lf, content='', score=1)
        with transaction.atomic():
            with self.assertRaises(ValidationError):
                LawFirmCalification.objects.create(owner=u1, target=self.main_lf, content='Hi!', score=5)
