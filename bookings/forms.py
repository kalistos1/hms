from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import  Booking, Reservation, Payment, Room, RoomServices,  AdditionalCharge
from accounts.models import User, Profile
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.db.models import Q
from django.utils import timezone

from django.core.exceptions import ValidationError


class DateInput(forms.DateInput):
    input_type = 'date'



class BasicUserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email', 'phone']
        
    def __init__(self, *args, **kwargs):
        super(BasicUserInfoForm, self).__init__(*args, **kwargs)
        
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder' :'Customer First name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder' :'Cusomer Last name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder' :'Customer Email'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'placeholder' :'Customer Phone No.'})


class ProfileInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['title', 'gender', 'date_of_birth','country', 'nationality', 'identity_type', 'id_no','city','state','address','occupation','image']
    
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={'class': 'form-control', 'placeholder': 'Country'}))
    nationality = CountryField(blank_label='(select nationality)').formfield(widget=CountrySelectWidget(attrs={'class': 'form-control', 'placeholder': 'Nationality'}))

    def __init__(self, *args, **kwargs):
        super(ProfileInfoForm, self).__init__(*args, **kwargs)
      
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder' :'Customer title'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control', 'placeholder' :'Customer Phone No.'})
        self.fields['date_of_birth'].widget = DateInput(attrs={'class': 'form-control', 'placeholder' :'Date Of Birth.'})
        self.fields['image'].widget.attrs.update({'class': 'form-control-file', 'placeholder' :'profile Pix.'})
        self.fields['identity_type'].widget.attrs.update({'class': 'form-control', 'placeholder' :'ID type.'})
        self.fields['id_no'].widget.attrs.update({'class': 'form-control', 'placeholder' :'Customers ID Number.'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'placeholder' :'Customers City'})
        self.fields['state'].widget.attrs.update({'class': 'form-control', 'placeholder' :'Customers State'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'placeholder' :'Customers Address.'})
        self.fields['occupation'].widget.attrs.update({'class': 'form-control', 'placeholder' :'Customers Occupation.'})
        
        



class BookingChoiceForm(forms.Form):
    CHOICES = [
        ('booking', 'Booking'),
        ('reservation', 'Reservation'),
    ]
    choice = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    
    def __init__(self, *args, **kwargs):
            super( BookingChoiceForm, self).__init__(*args, **kwargs)
        
            self.fields['choice'].widget.attrs.update({})



 
class RoomBookingForm(forms.ModelForm):
    
    class Meta:
        model = Booking
        fields = ['room', 'room_type', 'check_in_date', 'check_out_date', 'num_adults', 'num_children']
        widgets = {
            'check_in_date': DateInput(attrs={'class': 'form-control', 'placeholder': 'Check-in Date'}),
            'check_out_date': DateInput(attrs={'class': 'form-control', 'placeholder': 'Check-out Date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(RoomBookingForm, self).__init__(*args, **kwargs)
        
        # Filter rooms that are available
      
        
        # Update widget attributes for form fields
        self.fields['room_type'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Room Type'})
        self.fields['num_adults'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Number of Adults'})
        self.fields['num_children'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Number of Children'})
        self.fields['room'].widget.attrs.update({'class': 'form-control'})
        self.fields['room'].queryset = Room.objects.filter(is_available=True)
           
        



class RoomReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room', 'room_type', 'check_in_date', 'check_out_date', 'num_adults', 'num_children']
        widgets = {
            'check_in_date': DateInput(attrs={'class': 'form-control', 'placeholder': 'Check-in Date'}),
            'check_out_date': DateInput(attrs={'class': 'form-control', 'placeholder': 'Check-out Date'}),
        }

    def __init__(self, *args, **kwargs):
        super(RoomReservationForm, self).__init__(*args, **kwargs)
        self.fields['room_type'].widget.attrs.update({ 'class': 'form-control', 'placeholder': 'Room Type'})
        self.fields['num_adults'].widget.attrs.update({ 'class': 'form-control', 'placeholder': 'Number of Adults'})
        self.fields['num_children'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Number of Children'})
        self.fields['room'].widget.attrs.update({'class': 'form-control', })
        

   
class RoomServiceForm(forms.ModelForm):
    class Meta:
        model = RoomServices
        fields = ['service_type']
        widgets = {
            'service_type': forms.CheckboxSelectMultiple()  # Allow multiple selections or none
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service_type'].required = False  # Make room service optional


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'mode','status']
        
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs.update({ 'class': 'form-control', 'placeholder': 'Amount paid'})
        self.fields['mode'].widget.attrs.update({ 'class': 'form-control', 'placeholder': 'Mode Of Payment'})
        self.fields['status'].widget.attrs.update({ 'class': 'form-control', 'placeholder': ' Payment Status'})
        

class RoomServiceForm(forms.ModelForm):
    class Meta:
        model = RoomServices
        fields = ['room', 'service_type','price']
        
    def __init__(self, *args, **kwargs):
        super(RoomServiceForm, self).__init__(*args, **kwargs)
        self.fields['room'].widget.attrs.update({ 'class': 'form-control', 'placeholder': 'Room'})
        self.fields['service_type'].widget.attrs.update({ 'class': 'form-control', 'placeholder': 'Service Type'})
        self.fields['price'].widget.attrs.update({ 'class': 'form-control', 'placeholder': ' Price'})
        

class AdditionalChargeForm(forms.ModelForm):
    class Meta:
        model =  AdditionalCharge
        fields = ['category', 'description','amount']
        
    def __init__(self, *args, **kwargs):
        super(AdditionalChargeForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({ 'class': 'form-control', 'placeholder': 'Choose Category'})
        self.fields['description'].widget.attrs.update({ 'class': 'form-control', 'placeholder': 'Write a description of the service'})
        self.fields['amount'].widget.attrs.update({ 'class': 'form-control', 'placeholder': ' Price'})
        

