from django.urls import path
from .views import *

urlpatterns = [
    path('departments/', allDepartments, name='all_departments'),
    path('employees/', allEmployees, name='employees'),
    path('directors/', allDirectors, name='directors'),
    path('leave/', leave, name='leave'),
    # path('employees/register/', employee_registerview, name='register_employee'),
    path('employee/<str:id>/', employeeProfile, name='employee_profile'),
    path('director/<int:id>/', singleDirectorProfile, name='single_director_profile'),
    path('director-profile/', directorProfile, name='director_profile'),
    path('attendance/', attendance, name='attendance'),
    path('deprtment/attendance/', departmentattendance, name='department_attendance'),
    path('department/<slug:slug>/', singleDepartment, name='department'),
    path('department_leave/', department_leave, name='department_leave'),
    path('retirement/', retiring_staff, name='retirement'),
    path('approve_leave/<int:id>', approve_leave, name='approve_leave'),
    path('decline_leave/<int:id>', decline_leave, name='decline_leave'),
    path('director_activate/<uidb64>/<token>/', activate, name='director_activate'),
    path('employee_activate/<uidb64>/<token>/', employeeactivate, name='employee_activate'),
    path('search', searchview, name='search_employee'),

]
