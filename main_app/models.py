from django.db import models
from django.contrib.auth.models import User
import uuid as id_generator
import datetime

departments = (
    ("CS", "Computer Science"),
    ("BI", "Biology"),
    ("CH", "Chemistry"),
    ("EN", "English"),
    ("MA", "Mathematics"),
    ("PH", "Physics"),
    ("EC", "Economics"),
    ("PS", "Political Science"),
    ("HI", "History"),
    ("ED", "Education")
)

instructors = (
    ("Sarah Johnson", "Dr. Sarah Johnson"),
    ("Michael Lee", "Prof. Michael Lee"),
    ("Emily Davis", "Dr. Emily Davis"),
    ("Robert Brown", "Prof. Robert Brown"),
    ("Jessica Martinez", "Dr. Jessica Martinez"),
    ("William Smith", "Prof. William Smith"),
    ("Jennifer Wilson", "Dr. Jennifer Wilson"),
    ("David Anderson", "Prof. David Anderson"),
    ("Angela Thomas", "Dr. Angela Thomas"),
    ("Christopher Harris", "Prof. Christopher Harris")
)

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

class Course(models.Model):
    name = models.CharField(max_length=150)
    department = models.CharField(max_length=2, choices=departments, default=departments[0][0])
    instructor = models.CharField(max_length=100, choices=instructors, default=instructors[0][0]) 
    description = models.TextField(max_length=500)
    days = models.CharField(max_length=50, null=True)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    
    def __str__(self):
        return f'{self.department}: {self.name}'

class Enrollment(models.Model):
    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.student.name} is enrolled in {self.course.name}.'