from django.urls import path
from .views import Home, CreateStudentView, LoginView

urlpatterns = [
  path('', Home.as_view(), name='home_page'),
  path('students/register', CreateStudentView.as_view(), name='student-register'),
  path('users/login', LoginView.as_view(), name='user-login')
]