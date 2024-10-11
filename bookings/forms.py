from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import  Booking, Reservation, Payment, Room, RoomServices,  AdditionalCharge, RoomType,Hotel
from accounts.models import User, Profile
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ValidationError


class DateInput(forms.DateInput):
    input_type = 'date'


class HotelForm(forms.ModelForm):

    class Meta:
        model = Hotel
        fields = ['user','name','description', 'address','mobile','email','image']

    def __init__(self, *args, **kwargs):
        super(HotelForm, self).__init__(*args, **kwargs)
        
        self.fields['user'].widget.attrs.update({'class': 'form-control', 'placeholder' :'User'})
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder' :'Name'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder' :'Description'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'placeholder' :'Address'})
        self.fields['mobile'].widget.attrs.update({'class': 'form-control', 'placeholder' :'mobile'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder' :'email'})
        self.fields['image'].widget.attrs.update({'class': 'form-control', 'placeholder' :'pphoto'})


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
        fields = ['title', 'gender', 'date_of_birth','occupation']
    
    # country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={'class': 'form-control', 'placeholder': 'Country'}))
    # nationality = CountryField(blank_label='(select nationality)').formfield(widget=CountrySelectWidget(attrs={'class': 'form-control', 'placeholder': 'Nationality'}))

    def __init__(self, *args, **kwargs):
        super(ProfileInfoForm, self).__init__(*args, **kwargs)
      
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder' :'Customer title'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control', 'placeholder' :'Customer Phone No.'})
        self.fields['date_of_birth'].widget = DateInput(attrs={'class': 'form-control', 'placeholder' :'Date Of Birth.'})
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


# class RoomBookingForm(forms.ModelForm):
    
#     class Meta:
#         model = Booking
#         fields = ['room_type','room', 'check_in_date', 'check_out_date', 'num_adults', 'num_children']
        # widgets = {
        #     'check_in_date': DateInput(attrs={'class': 'form-control', 'placeholder': 'Check-in Date'}),
        #     'check_out_date': DateInput(attrs={'class': 'form-control', 'placeholder': 'Check-out Date'}),
        # }

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)
    #     super(RoomBookingForm, self).__init__(*args, **kwargs)
        
    #     # Update widget attributes for form fields
    #     self.fields['room'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['room'].queryset = Room.objects.filter(is_available=True)
    #     self.fields['room_type'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Room Type'})
    #     self.fields['num_adults'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Number of Adults'})
    #     self.fields['num_children'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Number of Children'})
       
   
class RoomBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room_type', 'room', 'check_in_date', 'check_out_date', 'num_adults', 'num_children']
        widgets = {
            'check_in_date': DateInput(attrs={'class': 'form-control', 'placeholder': 'Check-in Date'}),
            'check_out_date': DateInput(attrs={'class': 'form-control', 'placeholder': 'Check-out Date'}),
        }

    room_type = forms.ModelChoiceField(
        queryset=RoomType.objects.all(),
        widget=forms.Select(attrs={
            'hx-get': '/dashboard/get-available-rooms/',  # HTMX will make a GET request to this URL
            'hx-target': '#room-select',  # This is where the response will be placed
            'hx-trigger': 'change',  # Trigger the request on selection change
            'class': 'form-control',
        })
    )

    room = forms.ModelMultipleChoiceField(
        queryset=Room.objects.none(),  # Initially empty
        widget=forms.SelectMultiple(attrs={
            'id': 'room-select',
            'class': 'form-control',
            'hx-get': '/dashboard/get-room-price/',  # Fetch the price of selected room
            'hx-target': '#payment-amount',  # Response will update the amount field
            'hx-trigger': 'change',
            'hx-swap': 'outerHTML',
        })
    )

    def __init__(self, *args, **kwargs):
        room_type_id = kwargs.pop('room_type_id', None)
        super(RoomBookingForm, self).__init__(*args, **kwargs)
        
        if room_type_id:
            # Update the queryset for the room field based on the selected room_type
            self.fields['room'].queryset = Room.objects.filter(room_type_id=room_type_id, is_available=True)
        
        self.fields['num_adults'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Number of Adults'})
        self.fields['num_children'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Number of Children'})

   

class PaymentForm(forms.ModelForm):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Amount paid',
            'id': 'payment-amount'
        })
    )
    class Meta:
        model = Payment
        fields = ['amount', 'mode','status']
        
       
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        # self.fields['amount'].widget.attrs.update({ 'class': 'form-control', 'placeholder': 'Amount paid'})
        self.fields['mode'].widget.attrs.update({ 'class': 'form-control', 'placeholder': 'Mode Of Payment'})
        self.fields['status'].widget.attrs.update({ 'class': 'form-control', 'placeholder': ' Payment Status'})  
                                                  
                                                           
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
        

class PaymentCheckoutForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'status', 'mode']
        
    def __init__(self, *args, **kwargs):
        initial_amount = kwargs.pop('initial_amount', None)
        super().__init__(*args, **kwargs)
        
        if initial_amount is not None:
            self.fields['amount'].initial = initial_amount
        
        # Add Bootstrap classes to the form fields
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        self.fields['mode'].widget.attrs.update({'class': 'form-control'})
       
       
class UpdateCheckOutDateForm(forms.ModelForm):
    check_out_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="New Check-Out Date"
    )

    class Meta:
        model = Booking
        fields = ['check_out_date']

    def clean_check_out_date(self):
        new_check_out_date = self.cleaned_data.get('check_out_date')
        if new_check_out_date < timezone.now().date():
            raise forms.ValidationError("Check-out date cannot be in the past.")
        return new_check_out_date
    
    
    
    
# class RoomServiceForm(forms.ModelForm):
#     class Meta:
#         model = RoomServices
#         fields = ['service_type']
#         widgets = {
#             'service_type': forms.CheckboxSelectMultiple()  # Allow multiple selections or none
#         }
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['service_type'].required = False  # Make room service optional
