from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from califications.models import UserCalification
from lawfirms.models import LawFirm


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.username)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email='super@user.com', password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertIsNone(admin_user.username)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)


class CustomUserTests(TestCase):

    User = get_user_model()

    def test_user_creation(self):
        self.assertIsInstance(self.User.objects.create_user(email='user@sample.com', password='foo'), self.User)
        self.assertEqual(self.User.objects.all().count(), 1)
        with self.assertRaises(IntegrityError):
            self.assertIsInstance(self.User.objects.create_user(email='user@sample.com', password='foo'), self.User)

    def test_user_update(self):
        user = self.User.objects.create_user(email='user@sample.com', password='foo')
        self.assertEqual(user.email, 'user@sample.com')
        user.email = 'diferentuser@sample.com'
        user.save()
        self.assertEqual(user.email, 'diferentuser@sample.com')

    def test_performed_califications(self):
        main_user = self.User.objects.create_user(email='user@sample.com', password='foo')
        for i in range(20):
            user = self.User.objects.create_user(email='user{}@sample.com'.format(i), password='foo')
            UserCalification.objects.create(owner=main_user, target=user, score=3, content='lorem ipsum')
        self.assertEqual(main_user.performed_califications.all().count(), 20)

    def test_performed_cal_cascade_deletion(self):
        main_user = self.User.objects.create_user(email='user@sample.com', password='foo')
        for i in range(20):
            user = self.User.objects.create_user(email='user{}@sample.com'.format(i), password='foo')
            UserCalification.objects.create(owner=main_user, target=user, score=3, content='lorem ipsum')
        self.assertEqual(main_user.performed_califications.all().count(), 20)
        main_user.delete()
        self.assertEqual(main_user.performed_califications.all().count(), 0)

    def test_recived_califications(self):
        main_user = self.User.objects.create_user(email='user@sample.com', password='foo')
        for i in range(20):
            user = self.User.objects.create_user(email='user{}@sample.com'.format(i), password='foo')
            UserCalification.objects.create(owner=user, target=main_user, score=3, content='lorem ipsum')
        self.assertEqual(main_user.recived_califications.all().count(), 20)

    def test_recived_cal_cascade_deletion(self):
        main_user = self.User.objects.create_user(email='user@sample.com', password='foo')
        for i in range(20):
            user = self.User.objects.create_user(email='user{}@sample.com'.format(i), password='foo')
            UserCalification.objects.create(owner=user, target=main_user, score=3, content='lorem ipsum')
        self.assertEqual(main_user.recived_califications.all().count(), 20)
        main_user.delete()
        self.assertEqual(main_user.recived_califications.all().count(), 0)

    def test_working_in(self):
        main_user = self.User.objects.create_user(email='user@sample.com', password='foo')
        lf1 = LawFirm.objects.create(name='foo1', nit='100')
        lf2 = LawFirm.objects.create(name='foo2', nit='101')
        lf1.employees.add(main_user)
        self.assertEqual(main_user.working_in.all().count(), 1)
        lf2.employees.add(main_user)
        self.assertEqual(main_user.working_in.all().count(), 2)

    def test_working_in_deletions(self):
        main_user = self.User.objects.create_user(email='user@sample.com', password='foo')
        lf1 = LawFirm.objects.create(name='foo1', nit='100')
        lf2 = LawFirm.objects.create(name='foo2', nit='101')
        lf1.employees.add(main_user)
        self.assertEqual(main_user.working_in.all().count(), 1)
        lf2.employees.add(main_user)
        self.assertEqual(main_user.working_in.all().count(), 2)
        lf1.employees.clear()
        self.assertEqual(main_user.working_in.all().count(), 1)
        main_user.delete()
        self.assertEqual(lf2.employees.all().count(), 0)
