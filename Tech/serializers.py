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

class MContentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MContentsFile
        fields = ['fcontent']

class MContentSerializer(serializers.ModelSerializer):
    fcontents = MContentFileSerializer(many = True, read_only= True)

    class Meta:
        model = MContents
        fields = ['id','SCNum','SCName','performance','filetype','tcontent','bcontent','fcontents']

    def create(self, validated_data):
        fcontents_data = self.context['request'].FILES
        mcontents = MContents.objects.create(**validated_data)
        for fcontent_data in fcontents_data.getlist('fcontent'):
            MContentsFile.objects.create(mcontents=mcontents,fcontent=fcontent_data)
            print(mcontents)
        return mcontents

    '''def __init__(self, *args, **kwargs):
        super(MContentSerializer, self).__init__(*args, **kwargs)
        self.fields['fcontent'].required = False
'''

class MTaskUDSerializer(serializers.Serializer):
    class Meta:
        model = MTask
        fields = ['userdetail']

class DepartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['username','password']

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
