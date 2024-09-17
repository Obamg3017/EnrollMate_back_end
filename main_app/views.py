from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Student
from .serializers import StudentSerializer, UserSerializer

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