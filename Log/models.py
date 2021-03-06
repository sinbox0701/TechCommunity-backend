from django.db import models
from django.conf import settings
from django_enumfield import enum
from Tech.models import *
# Create your models here.

class DetailLog(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, null=True, blank=True)
    mtask = models.ForeignKey(MTask, on_delete=models.CASCADE, null=True, blank=True)
    mod = models.TextField(null=True, blank=True)
    userdetail = models.ForeignKey(UserDetail, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(null=True, blank=True, max_length=100)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    mc = models.IntegerField(null=True, blank=True)

    def datepublished(self):
        return self.date.strftime('%m/%d/%y %H:%M')

    def __str__(self):
        return self.performance.title + self.userdetail.user.username
