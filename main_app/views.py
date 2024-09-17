from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Student, Course, Enrollment
from .serializers import StudentSerializer, UserSerializer, CourseSerializer, EnrollmentSerializer

class CreateStudentView(generics.CreateAPIView):
  queryset = Student.objects.all()
  serializer_class = StudentSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=request.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data,
      'student': response.data,
    })


# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the course-collector api home route!'}
    return Response(content)
  
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      try:
        student = Student.objects.get(user=user)
        student_data = StudentSerializer(student).data
      except Student.DoesNotExist:
        student_data = None  
      
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data,
        'student': student_data  
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
  
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CourseSerializer
  
class EnrollmentList(generics.ListCreateAPIView):
  serializer_class = EnrollmentSerializer
  
  def get_queryset(self):
    student_data = self.request.user.student
    student = Student.objects.get(student_id=student_data.student_id)
    return Enrollment.objects.filter(student=student)
  
  def perform_create(self, serializer):
    student_data = self.request.user.student
    student = Student.objects.get(student_id=student_data.student_id)
    serializer.save(student=student)

class EnrollmentDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = EnrollmentSerializer
  lookup_field = 'id'

  def get_queryset(self):
    student_data = self.request.user.student
    student = Student.objects.get(student_id=student_data.student_id)
    return Enrollment.objects.filter(student=student)
  
  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    
    return Response({
      'enrollment': serializer.data
    })
  
  def perform_update(self, serializer):
    enrollment = self.get_object()
    if enrollment.student.student_id != self.request.user.student.student_id:
      raise PermissionDenied({"message": "You do not have permission to edit this enrollment"})
  
  def perform_destroy(self, instance):
    if instance.student.student_id != self.request.user.student.student_id:
      raise PermissionDenied({"message": "You do not have permission to delete this enrollment."})
    instance.delete()