from django.contrib import auth
from django.db import models


class AAIData(models.Model):
    user = models.OneToOneField(auth.get_user_model(), models.CASCADE, related_name='aai')
    organisation_name = models.CharField(max_length=200)


class MobilePhone(models.Model):
    aai = models.ForeignKey(AAIData, models.CASCADE, 'mobile')
    number = models.CharField(max_length=50)
