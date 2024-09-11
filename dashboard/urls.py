from django.urls import path
from . import views
app_name = "dashboard"


urlpatterns = [
    #dshboards
    
    path('admin_dash/',views.admin_dashboard, name="admin_dashboard"),
    path('supervisor_dash/',views.supervisor_dashboard, name ="supervisor_dashboard"),
    path('account_dash/',views.account_dashboard, name ="account_dashboard"),
    path('front_desk_dash/',views.frontdesk_dashboard, name ="frontdesk_dashboard"),
    
    #admin views
    # amenities
    path('admin/room-amenities/', views.admin_list_room_amenities, name='admin_list_room_amenities'),
    path('admin/room-amenities/create/', views.admin_create_room_amenity, name='admin_create_room_amenity'),
    path('admin/room-amenities/update/<int:pk>/', views.admin_update_room_amenity, name='admin_update_room_amenity'),
    path('admin/room-amenities/delete/<int:pk>/', views.admin_delete_room_amenity, name='admin_delete_room_amenity'),
    
    #room type
    path('admin/room-type/', views.admin_list_room_type, name='admin_list_room_types'),
    path('admin/room-type/create/', views.admin_create_room_type, name='admin_create_room_type'),
    path('admin/room-type/update/<int:pk>/', views.admin_update_room_type, name='admin_update_room_type'),
    path('admin/room-type/delete/<int:pk>/', views.admin_delete_room_type, name='admin_delete_room_type'),
  
   #room
    path('admin/rooms/', views.admin_list_room, name='admin_list_room'),
    path('admin/room/create/', views.admin_create_room, name='admin_create_room'),
    path('admin/room/update/<int:pk>/', views.admin_update_room, name='admin_update_room'),
    path('admin/room/delete/<int:pk>/', views.admin_delete_room, name='admin_delete_room'),
    
    
       #coupon
    path('admin/coupons/', views.admin_list_coupon, name='admin_list_coupon'),
    path('admin/couponcreate/', views.admin_create_coupon, name='admin_create_coupon'),
    path('admin/coupon/update/<int:pk>/', views.admin_update_coupon, name='admin_update_coupon'),
    path('admin/coupon/delete/<int:pk>/', views.admin_delete_coupon, name='admin_delete_coupon'),
    
    #Admin users
    path('admin/privilaged_users/list/', views.admin_users_list, name='admin_users_list'),
    path('admin/privilaged_user/create/', views.add_admin_privilaged_user, name='add_admin_privilaged_user'),
    path('admin/privilaged_user/delete/<int:pk>/', views.admin_delete_privilaged_user, name='admin_delete_privilaged_user'),


    #frontdesk
    path('front_desk/room_status/',views.frontdesk_room_status, name ="frontdesk_room_status"),
    path('front_desk/booking_list/',views.frontdesk_booking_list, name ="frontdesk_booking_list"),
    path('frontdesk/booking/', views.front_desk_booking, name='book_room'),
    path('frontdesk/reservation/', views.front_desk_reservation, name='reserve_room'),
    path('font_desk/receipt/<str:booking_id>/', views.receipt_view, name='receipt'),
    path('font_desk/re_receipt/<int:pk>/', views.re_issue_receipt_view, name='re_receipt'),
    path('frontdesk/add_booking_service/<int:pk>/', views.frontdesk_add_room_service, name="frontdesk_add_booking_service"),
    path('frontdesk/frontdesk_add_additional_charge/<int:pk>/', views.frontdesk_add_additional_charge, name="frontdesk_add_additional_charge"),

    path('frontdesk/checkout/<int:pk>/', views.checkout_view, name='checkout'),
    path('frontdesk/apply-coupon/<int:pk>/', views.frontdesk_apply_coupon_to_booking, name='apply_coupon'),
    path('frontdesk/checkout/payment/<int:pk>/', views.frontdesk_checkout_payment_view, name='checkout_payment'),
    
    
    
]
