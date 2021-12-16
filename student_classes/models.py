from django.db import models
from django.urls import reverse
# Create your models here.

class StudentClass(models.Model):
    department_name              =   models.CharField(max_length=100)
    department_code  =   models.CharField( max_length=4 ,help_text='Eg- ISE') 
    semester                 =   models.CharField(max_length=10, help_text='Eg- 1 semester')
    creation_date           =   models.DateTimeField(auto_now=False, auto_now_add=True)

    def get_absolute_url(self):
        return reverse('student_classes:class_list')

    def __str__(self):
        return "%s Section-%s"%(self.department_name, self.semester)
