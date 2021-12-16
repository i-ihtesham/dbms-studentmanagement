from django.forms import ModelForm
from django import forms
from .models import StudentClass

class StudentClassForm(ModelForm):
    class Meta:
        model = StudentClass
        exlude  =   'creation_date'
        fields = '__all__'
        widgets = {
            'department_name': forms.TextInput(attrs={'class': 'form-control'}),
            'department_code':  forms.TextInput(attrs={'class': 'form-control'}),
            'semester':  forms.TextInput(attrs={'class': 'form-control'}),
        }