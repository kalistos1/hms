from django import forms
from .models import * 
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 

class DateInput(forms.DateInput):
    input_type = 'date'



# login form
class LoginForm(forms.Form):    
        
    username = forms.CharField(
                 widget=forms.TextInput(attrs={ 
                                                    'class':'form-control'}))
    password = forms.CharField(
                 widget=forms.PasswordInput(attrs={
                                                   'class':'form-control'}))
                                                   
    
    

class SignUpForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)
    password2 = forms.CharField(required = True)
    t_and_c = forms.BooleanField(required=True)

   

    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            't_and_c',
          
            
        )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control', 'id':'name', 'placeholder':'First Name', 'id':'floatingInput', 'aria-describedby':'nameHelp'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control', 'id':'name', 'placeholder':'Last Name', 'id':'floatingInput','aria-describedby':'nameHelp'})
        self.fields['username'].widget.attrs.update({'class' : 'form-control', 'id':'name', 'placeholder':'Username'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control', 'id':'email', 'placeholder':'Email'})
        self.fields['password'].widget=forms.PasswordInput(attrs={'placeholder':'Password', 'class':'form form-control px-5', 'id':'pass'})
        self.fields['password2'].widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password', 'class':'form form-control px-5', 'id':'re_pass'})
        self.fields['t_and_c'].widget.attrs.update({'class' : 'custom-control-label',})
        
