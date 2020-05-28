from rest_framework import serializers
from .models import *

class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = '__all__'

class PerformanceCreateSerializer(serializers.Serializer):
    genre = serializers.CharField(label='genre', max_length=1000)
    title = serializers.CharField(label='title', max_length=1000)
    direction = serializers.CharField(label='direction', max_length=1000)
    construct = serializers.CharField(label='construct', max_length=1000)
    check = serializers.CharField(label='check', max_length=1000)
    date = serializers.CharField(label='date', max_length=1000)

class MTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = MTask
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'