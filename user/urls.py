from django.urls import path
from .views import *

urlpatterns = [
    path('register/', registerview, name='register'),
    path('login/', loginview, name='login'),
    path('logout/', logoutview, name='logout'),
    path('activate/<uidb64>/<token>/', activateview, name='activate'),
    path('resetpassword_validate/<uidb64>/<token>/', resetpassword_validateview, name='resetpassword_validate'),
    path('forgotpassword/', forgotpasswordview, name='forgotpassword'),
    path('reset-password/', resetpasswordview, name='reset-password'),

]
