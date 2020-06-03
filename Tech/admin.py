from django.contrib import admin
from .models import Department, UserDetail, Performance, DetailLog, Category, MContents, SContents,STask, MTask,Team, MContentsFile

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
admin.site.register(DetailLog)
admin.site.register(Team)

