from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Student
from .serializers import StudentSerializer

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
      'student': response.data,
    })


# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the course-collector api home route!'}
    return Response(content)