from django.db import models
from account.models import UserProfileInfo
from django.utils import timezone
from django.urls import reverse

gender_choices = ((1, 'Male'), (2, 'Female'))
Q_choices = ((1, 'Always'), (2, 'Sometimes'), (3, 'Usually'), (4, 'Often'), (5, 'Never'))

# Create your models here.

class Predictions(models.Model):
    profile = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE, related_name='predict')
    age = models.IntegerField()
    gender = models.IntegerField(choices=gender_choices, default=1)
    Q1 = models.IntegerField(choices=Q_choices, default=1)
    Q2 = models.IntegerField(choices=Q_choices, default=1)
    Q3 = models.IntegerField(choices=Q_choices, default=1)
    Q4 = models.IntegerField(choices=Q_choices, default=1)
    Q5 = models.IntegerField(choices=Q_choices, default=1)
    Q6 = models.IntegerField(choices=Q_choices, default=1)
    Q7 = models.IntegerField(choices=Q_choices, default=1)
    Q8 = models.IntegerField(choices=Q_choices, default=1)
    Q9 = models.IntegerField(choices=Q_choices, default=1)
    Q10 = models.IntegerField(choices=Q_choices, default=1)
    predicted_on = models.DateTimeField(default=timezone.now)
    num = models.IntegerField()

    def get_absolute_url(self):
        return reverse('predict: predict', kwargs={'pk': self.profile.pk})