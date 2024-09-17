from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    student_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
