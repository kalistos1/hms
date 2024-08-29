from django.shortcuts import render

# Create your views here.


#index view
def index(request):
    template ='pages/index.html'
    
    return render(request, template)

#about view
def about_us(request):
    template ='pages/about.html'
    
    return render(request, template)

#contac view
def contact_us(request):
    template ='pages/contact_us.html'
    
    return render(request, template)

#gallery view
def gallery(request):
    template ='pages/gallery.html'
    
    return render(request, template)