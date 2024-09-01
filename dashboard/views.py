from django.shortcuts import render

# Create your views here.

def admin_dashboard(request):
    template = "admin_user/dashboard.html"
    
    return render (request,template)


def supervisor_dashboard(request):
    template = "supervisor/dashboard.html"
    
    return render (request,template)


def account_dashboard(request):
    template = "account_officer/dashboard.html"
    
    return render (request,template)



def frontdesk_dashboard(request):
    template = "front_desk/dashboard.html"
    
    return render (request,template)


def frontdesk_room_status(request):
    template = "front_desk/roomstatus.html"
    
    return render (request,template)


def frontdesk_booking_list(request):
    template = "front_desk/bookinglist.html"
    
    return render (request,template)


def frontdesk_room_checkout(request):
    template = "front_desk/roomcheckout.html"
    
    return render (request,template)