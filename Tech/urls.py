from django.contrib import admin
from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from Tech import views as Tech_views

app_name = 'Tech'

urlpatterns = [
    path('', PeListView, name='list'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('add/', PeCreateView, name='add'),
    path('catask/<int:pk>', CaTaskView, name='catask1'),
    #path('catask/dep/<int:pk>', DepCreateView, name='dep'),
    path('delete/<int:pk>',PeDeleteView,name='delete'),
    path('catask/<int:pk>/<int:tnum>',TaskContentView,name='catask2'),
    path('catask/<int:pk>/<int:tnum>/<int:id>', ContentsUpdateView, name='coup'),
    path('catask/<int:pk>/<int:tnum>/<int:id>/file', fileupload, name='fileup')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)