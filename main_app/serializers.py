from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student, Course

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    
    class Meta:
        model = User
        fields = ['username']

class StudentSerializer(serializers.ModelSerializer):  
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Student
        fields = ['name', 'username', 'password', 'student_id', 'enrollment_year']
        read_only_fields = ['student_id', 'enrollment_year']

    def create(self, validated_data):
        username = validated_data.pop('user')['username']
        password = validated_data['password']
        user = User.objects.create_user(username=username, password=password)
        name=validated_data['name']
        
        student = Student.objects.create(
            user=user,
            name=name,
            )
        return student
class CourseSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Course
        fields = "__all__"
        read_only_fields = "name", "department", "instructor", "description"

         