from django.db import models
from django.db.models import Q
from django.forms import ValidationError
from lawfirms.models import LawFirm
from users.models import CustomUser as User


class UserCalification(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='performed_califications')
    date = models.DateTimeField(null=False, auto_now=True)
    score = models.FloatField()
    content = models.TextField(max_length=700)
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recived_califications', null=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        if (self.owner == self.target):
            raise ValidationError({'__all__': "The owner and target can't be the same"})
        if self.score > 5 or self.score < 1:
            raise ValidationError({'score': "The score must be a number between 1 and 5"})
        if self.content == '':
            raise ValidationError({'content': "The calification content can't be empty"})
        if len(self.content) < 10:
            raise ValidationError({'content': "The calification content length must be at least 10 characters long"})
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('owner', 'target'), name='unique_cal_per_user'),
            models.CheckConstraint(check=Q(score__gte=1) & Q(score__lte=5), name='score_restritions'),
            ]
        indexes = [models.Index(fields=['owner', 'target'])]
        get_latest_by = ['-date']
        ordering = ['-date']


class LawFirmCalification(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='performed_califications_lf')
    date = models.DateTimeField(null=False, auto_now=True)
    score = models.FloatField()
    content = models.TextField(max_length=700)
    target = models.ForeignKey(LawFirm, on_delete=models.CASCADE, related_name='califications', null=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        if (self.owner == self.target):
            raise ValidationError({'__all__': "The owner and target can't be the same"})
        if self.score > 5 or self.score < 1:
            raise ValidationError({'score': "The score must be a number between 1 and 5"})
        if len(self.content) < 10:
            raise ValidationError({'content': "The calification content length must be at least 10 characters long"})
        return super().clean()

    class Meta:
        constraints = [models.UniqueConstraint(fields=('owner', 'target'), name='unique_cal_per_lawfirm')]
        indexes = [models.Index(fields=['owner', 'target'])]
        get_latest_by = ['-date']
        ordering = ['-date']
