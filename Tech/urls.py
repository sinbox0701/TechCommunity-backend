from django.contrib import admin
from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from Tech import views as Tech_views

app_name = 'Tech'

urlpatterns = [
    path('', PeListView, name='list'),
    path('add/', PeCreateView, name='add'),
    path('category/<int:pk>', PeCateView, name='category'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)