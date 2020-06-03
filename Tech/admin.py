from django.contrib import admin

from .models import Department, UserDetail, Performance, Category, MContents, SContents,STask, MTask,TaskTeam, Comment,  MContentsFile


# Register your models here.

admin.site.register(Performance)
admin.site.register(Department)
admin.site.register(UserDetail)
admin.site.register(Category)
admin.site.register(SContents)
admin.site.register(MContents)
admin.site.register(MContentsFile)
admin.site.register(STask)
admin.site.register(MTask)
admin.site.register(TaskTeam)
admin.site.register(Comment)


