from django.db import models
from django.conf import settings
from django_enumfield import enum
from django.contrib.postgres.fields import JSONField
# Create your models here.

class Performance(models.Model): # 공연
    title = models.CharField(max_length=45, null=False)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.name

class Department(models.Model): # 부서
    name = models.CharField(max_length=10, null=False)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.name + "," + self.performance.title

class TaskTeam(models.Model): # 주관팀
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    TNum = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name + "," + self.performance.title


class UserDetail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    TNum = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username + "," + self.performance.title #+ "," + self.department.name

class FileType(enum.Enum):
    text = 0
    file = 1
    check = 2
    add = 3
    choice = 4


class SContents(models.Model): # 템플릿 콘텐츠
    SCName = models.CharField(max_length=100, null=True, blank=True) # 콘텐츠 이름
    filetype = enum.EnumField(FileType, default=FileType.text, null=True, blank=True) # 콘텐츠 파일 타입

    def __str__(self):
        return str(self.id) + "," + self.SCName

class MContents(models.Model): # 공연별 콘텐츠에 들어갈 내용
    SCNum = models.IntegerField(null=True,blank=True) # 템플릿 콘텐츠 에서 가져올 id
    SCName = models.CharField(max_length=100, null=True, blank=True) # 템플릿 콘텐츠에서 가져올 이름
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, null=True, blank=True)
    filetype = enum.EnumField(FileType, default=FileType.text, null=True, blank=True)  # 콘텐츠 파일 타입
    tcontent = models.TextField(null=True, blank=True) # 텍스트
    #fcontent = models.FileField(upload_to="files/", null=True, blank=True) # 파일
    bcontent = models.BooleanField(null=True, blank=True, default=0) # 선택사항

    def __str__(self):
        return str(self.id) + "," + str(self.SCNum) + "," + self.performance.title + "," + self.SCName

class MContentsFile(models.Model):
    mcontents = models.ForeignKey(MContents, on_delete=models.CASCADE)
    fcontent = models.FileField(upload_to="files/", null=True, blank=True)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE,null=True,blank=True)
    storage = models.CharField(max_length=1000, null=True, blank=True)
    name = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return str(self.mcontents.SCName) + "," + str(self.fcontent)

class STask(models.Model):
    TNum = models.IntegerField(null=False) # Task number
    DetNum = models.IntegerField(null=True, blank=True) # 업무항목 number
    SCNum = models.IntegerField(null=True, blank=True) # 템플릿 콘텐츠 id
    TName = models.CharField(max_length=40, null=False) # Task 이름
    DetName = models.CharField(max_length=40,null=True, blank=True) # 업무항목 이름
    objective = models.TextField(null=True, blank=True) # 목표
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    bool = models.BooleanField(null=True,blank=True,default=0) # 일반업무 = 0 회의업무 = 1
    Dbool = models.BooleanField(null=True,blank=True,default=0) # Task 만 => 1 Task+Det+Contents =>0
    team = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return str(self.id) + "," + str(self.TNum) + "," +  str(self.DetNum) + "," + str(self.SCNum) + "," + self.TName + "," + self.DetName

class statustyle(enum.Enum):
    none = 0
    ing = 1
    delay = 2
    finish = 3


class MTask(models.Model):
    TNum = models.IntegerField(null=True, blank=True)  # Task number
    DetNum = models.IntegerField(null=True, blank=True)  # 업무항목 number
    SCNum = models.IntegerField(null=True, blank=True)  # 템플릿 콘텐츠 id
    TName = models.CharField(max_length=40, null=True, blank=True)  # Task 이름
    DetName = models.CharField(max_length=40, null=True, blank=True)  # 업무항목 이름
    objective = models.TextField(null=True, blank=True)  # 목표
    category = models.IntegerField(null=True, blank=True)
    mcontents = models.ForeignKey(MContents, on_delete=models.CASCADE, null=True, blank=True) # Task 별 들어갈 콘텐츠
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, null=True, blank=True)
    team = models.CharField(max_length=40, null=True, blank=True) # 일반업무 시 : 업무팀    회의업무 시 : 업무 이름
    date = models.DateField(null=True, blank=True) # 일반업무에서는 마감 날짜 회의업무에서는 회의 날짜
    status = enum.EnumField(statustyle, default=statustyle.none, null=False) # 업무 상태
    place = models.TextField(null=True, blank=True) # 회의업무 시에 회의장소
    bool = models.IntegerField(null=True, blank=True, default=0)  # 일반업무 = 0 회의업무 = 1
    Dbool = models.IntegerField(null=True, blank=True,default=0)  # Task 만 => 1 Task+Det+Contents =>0


    def __str__(self):

        return self.performance.title + "," + str(self.id) + "," +  str(self.TNum) + "," + self.TName + "," + str(self.bool) + "," + str(self.Dbool)

class Comment(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, null=True, blank=True)
    userdetail = models.ForeignKey(UserDetail, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    parent = models.ForeignKey('self', related_name='reply', on_delete=models.CASCADE, null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    text = models.TextField()
    TNum = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return self.performance.title + "," + str(self.TNum)

'''
class PeCrTem(models.Model):
    genre = models.TextField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    direction = models.TextField(null=True, blank=True)
    construct = models.TextField(null=True, blank=True)
    check = models.TextField(null=True, blank=True)
    date = models.TextField(null=True, blank=True)'''