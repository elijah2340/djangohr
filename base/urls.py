from django.urls import path
from .views import *
from department.views import directorProfile

urlpatterns = [
    path('', adminDashboard, name='dashboard'),
]
