from rest_framework import serializers
from .models import *

class DetailLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailLog
        fields = '__all__'
