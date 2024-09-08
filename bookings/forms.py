from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import  Booking, Reservation, Payment, Room, RoomServices
from accounts.models import User, Profile
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class DateInput(forms.DateInput):
    input_type = 'date'



class BasicUserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone']
        
    def __init__(self, *args, **kwargs):
        super(BasicUserInfoForm, self).__init__(*args, **kwargs)
      
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder' :'Customer Email'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'placeholder' :'Customer Phone No.'})


class ProfileInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['title', 'gender', 'date_of_birth','country', 'nationality', 'identity_type', 'id_no']
    
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={'class': 'form-control', 'placeholder': 'Country'}))
    nationality = CountryField(blank_label='(select nationality)').formfield(widget=CountrySelectWidget(attrs={'class': 'form-control', 'placeholder': 'Nationality'}))

    def __init__(self, *args, **kwargs):
        super(ProfileInfoForm, self).__init__(*args, **kwargs)
      
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder' :'Customer title'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control-file', 'placeholder' :'Customer Phone No.'})
        self.fields['date_of_birth'].widget = DateInput(attrs={'class': 'form-control-file', 'placeholder' :'Date Of Birth.'})
        
        self.fields['identity_type'].widget.attrs.update({'class': 'form-control-file', 'placeholder' :'ID type.'})
        self.fields['id_no'].widget.attrs.update({'class': 'form-control', 'placeholder' :'Customers ID Number.'})



class BookingChoiceForm(forms.Form):
    CHOICES = [
        ('booking', 'Booking'),
        ('reservation', 'Reservation'),
    ]
    choice = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    
    def __init__(self, *args, **kwargs):
            super( BookingChoiceForm, self).__init__(*args, **kwargs)
        
            self.fields['choice'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Choose Booking or Reservation'})

            
            

class RoomBookingForm(forms.ModelForm):
    room = forms.ModelMultipleChoiceField(queryset=Room.objects.none(), widget=forms.CheckboxSelectMultiple)


    class Meta:
        model = Booking
        fields = ['room','room_type','check_in_date', 'check_out_date', 'num_adults', 'num_children']
        widgets = {
            'check_in_date': DateInput(attrs={'class': 'form-control', 'placeholder': 'Check-in Date'}),
            'check_out_date': DateInput(attrs={'class': 'form-control', 'placeholder': 'Check-out Date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(RoomBookingForm, self).__init__(*args, **kwargs)
       
        self.fields['room_type'].widget.attrs.update({ 'class': 'form-control', 'placeholder': 'Room Type'})
        self.fields['num_adults'].widget.attrs.update({ 'class': 'form-control', 'placeholder': 'Number of Adults'})
        self.fields['num_children'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Number of Children'})
        self.fields['room'].widget.attrs.update({'class': 'form-check-input', })

        # Dynamically filter the room choices
        if 'check_in_date' in self.data and 'check_out_date' in self.data:
            try:
                check_in_date = self.data.get('check_in_date')
                check_out_date = self.data.get('check_out_date')
                self.fields['room'].queryset = self.get_available_rooms(check_in_date, check_out_date)
            except (ValueError, TypeError):
                pass  # Invalid input, show no rooms
        else:
            self.fields['room'].queryset = Room.objects.none()

    def get_available_rooms(self, check_in_date, check_out_date):
        # Exclude rooms that are already booked during the selected dates
        booked_rooms = Booking.objects.filter(
            check_in_date__lt=check_out_date,
            check_out_date__gt=check_in_date
        ).values_list('room', flat=True)

        # Exclude rooms that are reserved during the selected dates
        reserved_rooms = Reservation.objects.filter(
            check_in_date__lt=check_out_date,
            check_out_date__gt=check_in_date
        ).values_list('room', flat=True)

        # Return rooms that are neither booked nor reserved
        return Room.objects.exclude(id__in=booked_rooms).exclude(id__in=reserved_rooms)
    
        

class RoomReservationForm(forms.ModelForm):
    room = forms.ModelChoiceField(queryset=Room.objects.none())
    
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
        self.fields['room'].widget.attrs.update({'class': 'form-check-input', })
        
        if 'check_in_date' in self.data and 'check_out_date' in self.data:
            try:
                check_in_date = self.data.get('check_in_date')
                check_out_date = self.data.get('check_out_date')
                self.fields['room'].queryset = self.get_available_rooms(check_in_date, check_out_date)
            except (ValueError, TypeError):
                pass  # Invalid input, show no rooms
        else:
            self.fields['room'].queryset = Room.objects.none()

    def get_available_rooms(self, check_in_date, check_out_date):
        # Exclude rooms that are already booked or reserved during the selected dates
        booked_rooms = Booking.objects.filter(
            check_in_date__lt=check_out_date,
            check_out_date__gt=check_in_date
        ).values_list('room', flat=True)

        reserved_rooms = Reservation.objects.filter(
            check_in_date__lt=check_out_date,
            check_out_date__gt=check_in_date
        ).values_list('room', flat=True)

        # Return rooms that are available
        return Room.objects.exclude(id__in=booked_rooms).exclude(id__in=reserved_rooms)

   
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
        
