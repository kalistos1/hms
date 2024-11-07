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
        


class AddAdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    is_admin = forms.BooleanField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name','username', 'email', 'password', 'is_admin','active_status',)

    def __init__(self, *args, **kwargs):
        super(AddAdminForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class':'form-control','placeholder':'First Name'}),
        self.fields['last_name'].widget.attrs.update({'class':'form-control','placeholder':'Last name'}),
        self.fields['username'].widget.attrs.update({'class':'form-control','placeholder':'Username'}),
        self.fields['email'].widget.attrs.update({'class':'form-control','placeholder':'Email'}),
        self.fields['password'].widget.attrs.update({'class':'form-control','placeholder':'Passsword'}),
        self.fields['is_admin'].widget.attrs.update({}),
        self.fields['active_status'].widget.attrs.update({}),
      
      
class AddSupervisorForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
   

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name','username', 'email', 'password', 'is_supervisor','active_status')

    def __init__(self, *args, **kwargs):
        super(AddSupervisorForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class':'form-control','placeholder':'First Name'}),
        self.fields['last_name'].widget.attrs.update({'class':'form-control','placeholder':'Last name'}),
        self.fields['username'].widget.attrs.update({'class':'form-control','placeholder':'Username'}),
        self.fields['email'].widget.attrs.update({'class':'form-control','placeholder':'Email'}),
        self.fields['password'].widget.attrs.update({'class':'form-control','placeholder':'Passsword'}),
        self.fields['is_supervisor'].widget.attrs.update({}),
        self.fields['active_status'].widget.attrs.update({}),
      
      
class AddFrontdeskForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name','username', 'email', 'password','is_frontdesk_officer','active_status',)

    def __init__(self, *args, **kwargs):
        super(AddFrontdeskForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class':'form-control','placeholder':'First Name'}),
        self.fields['last_name'].widget.attrs.update({'class':'form-control','placeholder':'Last name'}),
        self.fields['username'].widget.attrs.update({'class':'form-control','placeholder':'Username'}),
        self.fields['email'].widget.attrs.update({'class':'form-control','placeholder':'Email'}),
        self.fields['password'].widget.attrs.update({'class':'form-control','placeholder':'Passsword'}),
        self.fields['is_frontdesk_officer'].widget.attrs.update({}),
        self.fields['active_status'].widget.attrs.update({}),
      
      
class AddPosOfficerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
  
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name','username', 'email', 'password', 'is_pos_officer','active_status',)

    def __init__(self, *args, **kwargs):
        super(AddPosOfficerForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class':'form-control','placeholder':'First Name'}),
        self.fields['last_name'].widget.attrs.update({'class':'form-control','placeholder':'Last name'}),
        self.fields['username'].widget.attrs.update({'class':'form-control','placeholder':'Username'}),
        self.fields['email'].widget.attrs.update({'class':'form-control','placeholder':'Email'}),
        self.fields['password'].widget.attrs.update({'class':'form-control','placeholder':'Passsword'}),
        self.fields['is_pos_officer'].widget.attrs.update({}),
        self.fields['active_status'].widget.attrs.update({}),
      
  
         
class AddAccountOfficerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name','username', 'email', 'password', 'is_account_officer','active_status',)

    def __init__(self, *args, **kwargs):
        super(AddAccountOfficerForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class':'form-control','placeholder':'First Name'}),
        self.fields['last_name'].widget.attrs.update({'class':'form-control','placeholder':'Last name'}),
        self.fields['username'].widget.attrs.update({'class':'form-control','placeholder':'Username'}),
        self.fields['email'].widget.attrs.update({'class':'form-control','placeholder':'Email'}),
        self.fields['password'].widget.attrs.update({'class':'form-control','placeholder':'Passsword'}),
        self.fields['is_account_officer'].widget.attrs.update({}),
        self.fields['active_status'].widget.attrs.update({}),
      

class AddWorkerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)  # Allow password to be empty for updates

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'is_worker', 'active_status')

    def __init__(self, *args, **kwargs):
        super(AddWorkerForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['is_worker'].widget.attrs.update({})
        self.fields['active_status'].widget.attrs.update({})

    def save(self, commit=True):
        user = super().save(commit=False)
        # If the password field is filled, hash it
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
   
  
   