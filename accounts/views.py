
from decimal import Decimal
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.hashers import make_password
from django.contrib import messages



def signin(request):
    if request.user.is_authenticated:
        return redirect(get_dashboard_url(request.user))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            
            if user is not None:
                login(request, user)
                return redirect(get_dashboard_url(user))
            
            else:
                messages.error(request, 'Invalid login details')
        else:
            messages.error(request, 'Invalid login details')
    else:
        form = LoginForm()

    return render(request, 'pages/signin.html', {'form': form})



# sign up view
def sign_up(request):
    template = "pages/signup.html"
  
    if request.method == 'POST':
        form =  SignUpForm(request.POST)
        
        if form.is_valid(): 

            cd = form.cleaned_data
            get_firstname = cd['first_name']
            get_lastname =cd['last_name']
            get_email = cd['email']
            get_username =cd['username']
            get_password1 = cd['password']
            get_password2 = cd['password2']
            get_t_and_c = cd['t_and_c']
                     
            if User.objects.filter(username=get_username).exists():
                messages.error(request, 'Error username already Exists')
                return redirect('auth:signup')

            elif User.objects.filter(email=get_email).exists():
                messages.error(request, 'Error Email already Exists')
                return redirect('auth:signup')

            elif get_password1 != get_password2:
                messages.error(request, 'passwords does not match')
                return redirect('auth:signup')
            
            elif get_t_and_c != True:
                messages.error(request, 'To Signup, agree to aour terms and conditions')
                return redirect('authentication:signup')
                     
            else:
                
                user = User.objects.create(password = make_password(get_password1), first_name = get_firstname, last_name = get_lastname, username = get_username, email = get_email, t_and_c = get_t_and_c)             
                messages.error(request, 'signup was successful. please login')
                return redirect('auth:signin')                             
        else:

            messages.error(request, 'unable create to create user, check your credentials')
            return redirect('auth:signup')
           
    form=SignUpForm()
    context ={
              'form': form
        }
    return render(request, template, context)
   


@login_required
def signout(request):
    logout(request)
    return redirect('core:index')



def get_dashboard_url(user):
    if user.is_admin:
        return 'dashboard:admin_dashboard'
    elif user.is_supervisor:
        return 'dashboard:supervisor_dashboard'
    elif user.is_account_officer:
        return 'dashboard:account_dashboard'
    elif user.is_frontdesk_officer:
        return 'dashboard:frontdesk_dashboard'
    elif user.is_pos_officer:
        return 'dashboard:pos_user_dashboard'
    else:
        return 'core:index'
    