from .models import *
from django import forms
from django.forms import ModelForm
from .models import *

class FileCForm(ModelForm):
    class Meta:
        model = MContents
        fields = ['SCNum','SCName', 'performance','fcontent']

    def __init__(self, *args, **kwargs):
        super(FileCForm, self).__init__(*args, **kwargs)
        self.fields['fcontent'].required = False

class PerformanceForm(forms.ModelForm):
    class Meta:
        model = Performance
        fields = ['title']

class PerCreateForm(forms.Form):
    genre = forms.CharField(label='genre', max_length=1000)
    title = forms.CharField(label='title', max_length=1000)
    directiont = forms.CharField(label='title', max_length=1000)
    #directionf = forms.FileField(label='',upload_to="files/")
    configurationt = forms.CharField(label='configurationt', max_length=1000)
    #configurationf = forms.FileField(label='configurationf',upload_to="files/")
    check = forms.CharField(label='check', max_length=1000)
    date = forms.CharField(label='date', max_length=1000)
    place = forms.CharField(label='place', max_length=1000)
    special  = forms.CharField(label='special', max_length=1000)
    #drawing = forms.FileField(label='drawing',upload_to="files/")

'''    def __init__(self, *args, **kwargs):
        super(PerCreateForm, self).__init__(*args, **kwargs)
        self.fields['direction'].required = False
        self.fields['configuration'].required = False
        self.fields['drawing'].required = False'''

