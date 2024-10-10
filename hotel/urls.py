from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('auth/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('hrm/', include('hrm.urls')),
    path('booking/', include('bookings.urls')),
    path('inventory/', include('inventory.urls')),
    
    #ckeditor 5
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    
    #pos
    path('pos/', include('pos.urls')),
    
     #accounting
    path('accounting/', include('accounting.urls')),

]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)