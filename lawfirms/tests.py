from random import randint

from califications.models import LawFirmCalification
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from lawfirms.models import Employee, LawFirm


class LawFirmTests(TestCase):

    User = get_user_model()
    content = 'lorem ipsum dolor sit amet'

    def test_create_LawyerFirm(self):
        user = self.User.objects.create_user(email='generic@sample.com', password='foo')
        lf = LawFirm.objects.create(name='foo', nit='100', legalrep=user)
        self.assertEqual(lf.name, 'foo')
        self.assertEqual(lf.legalrep, user)
        self.assertEqual(lf.nit, '100')

    def test_invalid_values(self):
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                LawFirm.objects.create(name=None, nit='100')
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                LawFirm.objects.create(name='foo', nit=None)

    def test_califications_3_entries_score(self):
        user = self.User.objects.create_user(email='generic1@sample.com', password='foo')
        lf = LawFirm.objects.create(name='foo', nit='100')
        lf.califications.add(LawFirmCalification.objects.create(score=5, owner=user, content=self.content, target=lf))
        self.assertEqual(len(lf.latest_califications()), 1)
        user = self.User.objects.create_user(email='generic2@sample.com', password='foo')
        lf.califications.add(LawFirmCalification.objects.create(score=3, owner=user, content=self.content, target=lf))
        self.assertEqual(len(lf.latest_califications()), 2)
        self.assertEqual(lf.cal_score(), 4)
        user = self.User.objects.create_user(email='generic3@sample.com', password='foo')
        lf.califications.add(LawFirmCalification.objects.create(score=1, owner=user, content=self.content, target=lf))
        user = self.User.objects.create_user(email='generic4@sample.com', password='foo')
        lf.califications.add(LawFirmCalification.objects.create(score=2, owner=user, content=self.content, target=lf))
        self.assertEqual(lf.cal_score(), 2.75)

    def test_califications_100_entries_score(self):
        lf = LawFirm.objects.create(name='foo', nit='100')
        score = 0
        for i in range(1, 101):
            user = self.User.objects.create_user(email='generic{}@sample.com'.format(i), password='foo')
            aux = randint(1, 5)
            lf.califications.add(LawFirmCalification.objects.create(score=aux, owner=user, content=self.content, target=lf))
            score += aux
        self.assertEqual(score/100, lf.cal_score())

    def test_func_latest_califications(self):
        lf = LawFirm.objects.create(name='foo', nit='100')
        for i in range(100):
            user = self.User.objects.create_user(email='generic{}@sample.com'.format(i), password='foo')
            lf.califications.add(LawFirmCalification.objects.create(score=3, owner=user, content=self.content, target=lf))
        self.assertEqual(len(lf.latest_califications(12)), 12)
        self.assertEqual(len(lf.latest_califications(100)), 50)
        self.assertEqual(len(lf.latest_califications()), 10)
        self.assertEqual(lf.latest_califications(5)[0].pk, user.performed_califications_lf.all()[0].pk)
        user = self.User.objects.get(email='generic89@sample.com')
        self.assertEqual(lf.latest_califications(20)[10].pk, user.performed_califications_lf.all()[0].pk)


class LawFirmRelationsTests(TestCase):

    User = get_user_model()

    def setUp(self):
        self.time = timezone.now().date()
        self.lf = LawFirm.objects.create(name='foo', nit='100', legalrep=None)
        self.u1 = self.User.objects.create_user(email='user1@sample.com', password='foo')
        self.u2 = self.User.objects.create_user(email='user2@sample.com', password='foo')
        self.u3 = self.User.objects.create_user(email='user3@sample.com', password='foo')
        return super().setUp()

    def test_user_vinculation(self):
        self.lf.employees.add(self.u1, through_defaults={'date_joined': self.time})
        self.assertEqual(self.lf.employees.all().count(), 1)
        self.assertEqual(Employee.objects.all().count(), 1)

    def test_multiple_vinculations(self):
        self.lf.employees.add(self.u1, self.u2, self.u3)
        self.assertEqual(Employee.objects.filter(lawfirm=self.lf).count(), 3)
        self.assertEqual(Employee.objects.get(user=self.u3).date_joined, self.time)

    def test_extra_fields(self):
        Employee.objects.create(lawfirm=self.lf, user=self.u1, position='Lawyer', email='lawfirm.u1@sample.com')
        self.assertEqual(self.lf.employees.all().count(), 1)
        self.assertEqual(self.lf.employees.all()[0].email, 'lawfirm.u1@sample.com')
