from django.db import models
from django.db.models import Avg
from django.utils import timezone
from users.models import CustomUser as User


class LawFirm(models.Model):
    
    name = models.CharField(max_length=200, null=False)
    nit = models.CharField(max_length=200, null=False)
    webpage = models.URLField(null=True)
    legalrep = models.ForeignKey(User, null=True, editable=True, on_delete=models.SET_NULL, related_name='legal_rep')
    employees_info = models.ManyToManyField(User, through='Employee')
    email = models.EmailField(null=False)

    def cal_score(self):
        return self.califications.aggregate(Avg('score'))['score__avg']

    def latest_califications(self, amount=10):
        if amount > 50:
            amount = 50
        elif amount < 1:
            amount = 1
        return self.califications.all()[:amount]

    class Meta:
        verbose_name = 'LawFirm'
        verbose_name_plural = 'LawFirms'


class Employee(models.Model):

    lawfirm = models.ForeignKey(LawFirm, on_delete=models.CASCADE, related_name='employees')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='working_in')
    date_joined = models.DateField(default=timezone.now)
    position = models.CharField(max_length=200, null=False)
    email = models.EmailField(null=True)    

    class Meta:
        indexes = [
            models.Index(fields=['lawfirm', 'user'])
            ]
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
