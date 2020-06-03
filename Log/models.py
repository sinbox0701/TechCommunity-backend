from django.db import models
from django.conf import settings
from django_enumfield import enum
from Tech.models import *
# Create your models here.

class DetailLog(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, null=True, blank=True)
    mtask = models.ForeignKey(MTask, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    mod = models.TextField(null=True, blank=True)
    userdetail = models.ForeignKey(UserDetail, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.performance.title + "," + self.mtask.mcontents.SCName + "," + self.mod + "," + str(self.update)
