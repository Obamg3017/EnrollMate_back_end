from django.db import models
from django.contrib.auth.models import User
import uuid as id_generator
import datetime

class Student(models.Model):
    student_id = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    name = models.CharField(max_length=100)
    enrollment_year = models.PositiveIntegerField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.enrollment_year:
            self.enrollment_year = datetime.datetime.now().year
        if not self.student_id:
            self.student_id = self.generate_SIS_id()
        super(Student, self).save(*args, **kwargs)
    
    def generate_SIS_id(self):
        new_id = str(id_generator.uuid4().int)[:6]
        return f'{self.enrollment_year}{new_id}'
    
    def __str__(self):
        return f'{self.name} has student id: {self.student_id}'