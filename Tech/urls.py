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
    path('catask/<int:pk>', CaTaskView, name='catask'),
    path('delete/<int:pk>',PeDeleteView,name='delete'),
    path('catask/taco/<int:pk>/<int:tnum>',TaskContentView,name='taco'),
    path('catask/taco/<int:pk>/<int:tnum>/<int:id>', ContentsUpdateView, name='coup'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)