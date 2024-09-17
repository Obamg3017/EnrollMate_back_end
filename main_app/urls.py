from django.urls import path
from .views import Home, CreateStudentView

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('students/register', CreateStudentView.as_view(), name='student-register')
]