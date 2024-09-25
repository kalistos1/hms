from django.urls import path
from . import views


app_name = "hrm"

urlpatterns = [
    path('departments/', views.department_list, name='departments'),
    path('departments/create_department/', views.department_create, name='department_create'),
    path('departments/delete_department/<int:pk>/', views.department_delete, name='department_delete'),
    path('departments/update_department/<int:pk>/', views.department_update, name='department_update'),
    
    path('departments/locations/', views.department_location_list, name='department_locations'),
    path('departments/create_locations', views.department_location_create, name='department_locations_create'),
    path('departments/delete_locations/<int:pk>/', views.department_location_delete, name='department_locations_delete'),
    path('departments/update_locations/<int:pk>/', views.department_location_update, name='department_locations_update'),
    
    path('departments/employees/', views.employee_list, name='employees'),
    path('departments/create_employee', views.employee_create, name='employee_create'),
    path('departments/delete_employee/<int:pk>/', views.employee_delete, name='employee_delete'),
    path('departments/update_employee/<int:pk>/', views.employee_update, name='employee_update'),
    
    path('departments/schedules/', views.staff_schedule_list, name='staff_schedule'),
    path('departments/create_schedule/', views.staff_schedule_create, name='schedule_create'),
    path('departments/delete_schedule/<int:pk>/', views.staff_schedule_delete, name='schedule_delete'),
    path('departments/update_schedule/<int:pk>/', views.staff_schedule_update, name='schedule_update'),
    
    path('check-in/', views.check_in, name='check_in'),
    path('check-out/', views.check_out, name='check_out'),
]
