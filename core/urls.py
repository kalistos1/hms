from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    
    #frontpages
    path ('', views.index, name="index"),
    path ('about/', views.about_us, name="about"),
    path ('contact_us/', views.contact_us, name="contact"),
    path ('gallery/', views.gallery, name="gallery"),
    path('roomtype/room_list/<slug:slug>/', views.room_list, name='room_type_list'),
    
]
