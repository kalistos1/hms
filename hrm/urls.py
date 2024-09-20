from django.urls import path
from . import views


app_name = "hrm"

urlpatterns = [
    path('departments/', views.department_list, name='departments'),
    path('departments/create_department/', views.department_create, name='department_create'),
    path('check-in/', views.check_in, name='check_in'),
    path('check-out/', views.check_out, name='check_out'),
]
