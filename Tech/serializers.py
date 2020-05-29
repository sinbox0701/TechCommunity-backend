from rest_framework import serializers
from .models import *

class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = '__all__'

class PerformanceCreateSerializer(serializers.Serializer):
    genre = serializers.CharField(label='genre', max_length=1000)
    title = serializers.CharField(label='title', max_length=1000)
    directiont = serializers.CharField(label='title', max_length=1000)
    # directionf = serializers.FileField(label='',upload_to="files/")
    configurationt = serializers.CharField(label='configurationt', max_length=1000)
    # configurationf = serializers.FileField(label='configurationf',upload_to="files/")
    check = serializers.CharField(label='check', max_length=1000)
    date = serializers.CharField(label='date', max_length=1000)
    place = serializers.CharField(label='place', max_length=1000)
    special = serializers.CharField(label='special', max_length=1000)
    # drawing = serializers.FileField(label='drawing',upload_to="files/")


class MTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = MTask
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MContents
        fields = '__all__'

class MTaskUDSerializer(serializers.Serializer):
    class Meta:
        model = MTask
        fields = ['userdetail']
