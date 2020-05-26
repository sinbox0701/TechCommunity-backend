from django.db import models
from django.conf import settings
from django_enumfield import enum
from django.contrib.postgres.fields import JSONField
# Create your models here.

class Performance(models.Model):
    title = models.CharField(max_length=45, null=False)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=10, null=False)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.name + "," + self.performance.title

class UserDetail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username + "," + self.performance.title + "," + self.department.name

class FileType(enum.Enum):
    text = 0
    file = 1
    check = 2
    add = 3
    choice = 4


class SContents(models.Model):
    SCName = models.CharField(max_length=100, null=True, blank=True)
    filetype = enum.EnumField(FileType, default=FileType.text, null=True, blank=True)

    def __str__(self):
        return self.SCName

class MContents(models.Model):
    SCNum = models.IntegerField(null=False)
    SCName = models.CharField(max_length=100, null=True, blank=True)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, null=True, blank=True)
    tcontent = models.TextField(null=True, blank=True)
    fcontent = models.FileField(upload_to="files/", null=True, blank=True)
    bcontent = models.BooleanField(null=True, blank=True, default=0)

    def __str__(self):
        return self.performance.title + "," + self.SCName

class STask(models.Model):
    TNum = models.IntegerField(null=False)
    DetNum = models.IntegerField(null=False)
    SCNum = models.IntegerField(null=True, blank=True)
    TName = models.CharField(max_length=40, null=False)
    DetName = models.CharField(max_length=40, null=False)
    objective = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.id + "," + self.TNum + "," +  self.DetNum + "," + self.SCNum + "," + self.TName + "," + self.DetName


class MTask(models.Model):
    TNum = models.IntegerField(null=True, blank=True)
    DetNum = models.IntegerField(null=True, blank=True)
    TName = models.CharField(max_length=40, null=False)
    DetName = models.CharField(max_length=40, null=False)
    mcontents = models.ForeignKey(MContents, on_delete=models.CASCADE, null=True, blank=True)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True,blank=True)
    userdetail = models.ForeignKey(UserDetail, on_delete=models.CASCADE, null=True, blank=True)
    endDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.id + "," +  self.TNum + "," + self.DetNum + "," + self.mcontents.id + "," + self.TName + "," + self.DetName


class DetailLog(models.Model):
    mtask = models.ForeignKey(MTask, on_delete=models.CASCADE, null=True, blank=True)
    update = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    mod = models.TextField(null=True, blank=True)
    userdetail = models.ForeignKey(UserDetail, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.mtask.mcontents.SCName + "," + self.mod + "," + self.update


class PeCrTem(models.Model):
    genre = models.TextField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    direction = models.TextField(null=True, blank=True)
    construct = models.TextField(null=True, blank=True)
    check = models.TextField(null=True, blank=True)
    date = models.TextField(null=True, blank=True)