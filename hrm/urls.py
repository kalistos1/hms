from django.urls import path
from . import views


app_name = "hrm"

urlpatterns = [
    path('quick_link/', views.hrm_quick_links, name='quick_links'),
    path('departments/', views.department_list, name='departments'),
    path('departments/create_department/', views.department_create, name='department_create'),
    path('departments/delete_department/<int:pk>/', views.department_delete, name='department_delete'),
    path('departments/update_department/<int:pk>/', views.department_update, name='department_update'),
    path('departments/update-form/<int:pk>/', views.admin_update_department_form, name='admin_update_department_form'),

    path('departments/locations/', views.department_location_list, name='department_locations'),
    path('departments/create_locations', views.department_location_create, name='department_locations_create'),
    path('departments/delete_locations/<int:pk>/', views.department_location_delete, name='department_locations_delete'),
    path('departments/update_locations/<int:pk>/', views.department_location_update, name='department_locations_update'),
    path('departments/location-update-form/<int:pk>/', views.admin_update_department_location_form, name='admin_update_department_location_form'),

    path('departments/employees/', views.employee_list, name='employees'),
    path('departments/create_employee', views.employee_create, name='employee_create'),
    path('departments/delete_employee/<int:pk>/', views.employee_delete, name='employee_delete'),
    path('departments/update_employee/<int:pk>/', views.employee_update, name='employee_update'),
    path('departments/employee-update-form/<int:pk>/', views.admin_update_employee_form, name='admin_update_employee_form'),


    path('departments/schedules/', views.staff_schedule_list, name='staff_schedule'),
    path('department/current_staff_schedule',views.current_schedule_list, name ="current_schedule_list"),
    path('departments/create_schedule/', views.staff_schedule_create, name='schedule_create'),
    path('departments/delete_schedule/<int:pk>/', views.staff_schedule_delete, name='schedule_delete'),
    path('departments/update_schedule/<int:pk>/', views.staff_schedule_update, name='schedule_update'),
    path('departments/schedule-update-form/<int:pk>/', views.admin_update_schedule_form, name='admin_update_schedule_form'),

    path('departments/daily_attendance/', views.admin_worker_attendance, name='daily_attendance'),

    #old
    path('departments/checkout_attendance/<int:pk>/', views.checkout_employee, name='checkout_employee'),
    
    path('check-in/', views.check_in, name='check_in'),
    path('supervisor_checkin_employee/<int:pk>/', views.supervisor_check_in_employee, name='supervisor_check_in_employee'),
    path('check-out/', views.check_out, name='check_out'),
    
    #new
    path('supervisor_checkout_employee/<int:pk>/', views.check_out_employee, name='supervisor_checkout_employee'),
]
