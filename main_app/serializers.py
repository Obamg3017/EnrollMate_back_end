from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student, Course, Enrollment

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
    department_display = serializers.SerializerMethodField()
    instructor_display = serializers.SerializerMethodField()
    
    class Meta: 
        model = Course
        fields = ["id", "name", "department", "department_display", "instructor", "instructor_display", "description", "days", "start", "end"]
        read_only_fields = ("id", "name", "department", "department_display", "instructor", "instructor_display", "description", "days", "start", "end")
        
    def get_department_display(self, obj):
        return obj.get_department_display()
    
    def get_instructor_display(self, obj):
        return obj.get_instructor_display()

class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True)
    
    class Meta:
        model = Enrollment
        fields = ["id", 'student', 'course', 'course_id']

    def create(self, validated_data):
        course = validated_data.pop('course_id')
        enrollment = Enrollment.objects.create(course=course, **validated_data)
        return enrollment