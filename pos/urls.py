from django.urls import path
from .import views

app_name ="pos"

urlpatterns = [
    
]

htmx_views =[
    path('ordering/',  views.pos_index, name='products'),
    path('products/<slug:slug>/', views.category_products_view, name='category-products'),
]

urlpatterns += htmx_views