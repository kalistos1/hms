from django.shortcuts import render, get_object_or_404
from .models import *

# Create your views here.


def pos_index(request, slug=None):
    categories = ProductCategory.objects.all()
    context ={
        'categories':categories,
        'current_slug': slug 
    }
    return render (request, 'pages/pos_index.html',context)



# HTMX view to load products based on category
def category_products_view(request, slug):
    category = get_object_or_404(ProductCategory, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'partials/htmx/product_list.html', {'products': products})