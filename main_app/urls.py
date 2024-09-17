from django.urls import path
from .views import Home, CreateStudentView, LoginView, CourseListView, EnrollmentList, EnrollmentDetail

urlpatterns = [
  path('', Home.as_view(), name='home_page'),
  path('students/register', CreateStudentView.as_view(), name='student-register'),
  path('users/login', LoginView.as_view(), name='user-login'),
  path('students/courses', CourseListView.as_view(), name='course-list'),
  path('students/<int:id>/enrollments', EnrollmentList.as_view(), name='enrollment-list-create'),
  path('students/<int:student_id>/enrollments/<int:id>', EnrollmentDetail.as_view(), name='enrollment-detail')
]