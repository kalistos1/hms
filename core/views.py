from django.shortcuts import render, get_object_or_404
from bookings.models import *

# Create your views here.


#index view
def index(request):
    template ='pages/index.html'
    
    room_types = RoomType.objects.all()
    context = {
        'room_types':room_types,
    }
    
    return render(request, template, context)




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


#gallery view
def room_list(request,slug):
    
    template ='pages/roomlist.html'
    
    room_type = get_object_or_404(RoomType, slug=slug)
    rooms = Room.objects.filter(room_type=room_type)
    amenities = room_type.amenities.all()
  
    
    context = {
     'room_type': room_type,
     'rooms': rooms,
     'amenities': amenities
     }
    
    return render(request, template, context)