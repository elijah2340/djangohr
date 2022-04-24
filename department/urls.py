from django.urls import path
from .views import *

urlpatterns = [
    path('departments/', allDepartments, name='all_departments'),
    path('employees/', allEmployees, name='employees'),
    path('leave/', leave, name='leave'),
    # path('employees/register/', employee_registerview, name='register_employee'),
    path('employee/<str:id>/', employeeProfile, name='employee_profile'),
    path('attendance/', Attendance_New.as_view(), name='attendance'),
    path('attendance/<int:pk>/out/', Attendance_Out.as_view(), name='attendance_out'),
    path('<slug:slug>/', singleDepartment, name='department'),
]
