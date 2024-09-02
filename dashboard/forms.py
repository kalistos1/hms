from django import forms
from bookings.models import  Booking, Room
from accounts.models import  User, Profile
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class DateInput(forms.DateInput):
    input_type = 'date'


class CustomerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        
    title = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=100, required=True)
    date_of_birth = forms.DateField(widget=DateInput())
    gender = forms.ChoiceField(choices=Profile.GENDER, required=True)
    country =  CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={'class': 'form-control', 'placeholder': 'Country'}))
    nationality = CountryField(blank_label='(select Nationality)').formfield(widget=CountrySelectWidget(attrs={'class': 'form-control', 'placeholder': 'Nationality'}))
    image = forms.ImageField(required=False)
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True)
    address = forms.CharField(max_length=1000, required=True)
    occupation = forms.CharField(max_length=1000)
    id_no = forms.CharField(max_length=1000, required=False)
    identity_type = forms.ChoiceField(choices=Profile.IDENTITY_TYPE, required=False)
    identity_image_front = forms.ImageField(required=False)
    identity_image_back = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Mr.'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Mobile No'})
        self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Date of Birth'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Gender'})
        self.fields['country'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Country'})
        self.fields['nationality'].widget.attrs.update({'placeholder': 'Country'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'placeholder': 'City'})
        self.fields['state'].widget.attrs.update({'class': 'form-control', 'placeholder': 'State'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Address'})
        self.fields['occupation'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Occupation'})
        self.fields['id_no'].widget.attrs.update({'class': 'form-control', 'placeholder': 'ID Number'})
        self.fields['identity_type'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Identity Type'})
        self.fields['identity_image_front'].widget.attrs.update({'class': 'form-control-file', 'placeholder': 'Upload Front Image'})
        self.fields['identity_image_back'].widget.attrs.update({'class': 'form-control-file', 'placeholder': 'Upload Back Image'})
        self.fields['image'].widget.attrs.update({'class': 'form-control-file', 'placeholder': 'Upload profile image'})




class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_type', 'room_type','room','check_in_date', 'check_out_date', 'num_adults', 'num_children', 'advance_amount','discount_type','discount_amount','payment_mode', 'vip', 'total', 'payment_status','total','arrival_from']

    room = forms.ModelMultipleChoiceField(queryset=Room.objects.filter(is_available=True), required=True)

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
       
        self.fields['check_in_date'].widget = DateInput(attrs={'class': 'form-control','placeholder': 'Check-In Date'})
        self.fields['check_out_date'].widget = DateInput(attrs={'class': 'form-control','placeholder': 'Check-Out Date'})
        self.fields['booking_type'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Booking Type'})
        self.fields['arrival_from'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Arrival From'})
        self.fields['room_type'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Room Type'})
        self.fields['room'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Room'})
        self.fields['num_adults'].widget.attrs.update({'class': 'form-control', 'placeholder': 'No. Adults'})
        self.fields['num_children'].widget.attrs.update({'class': 'form-control', 'placeholder': 'No. Children'})
        self.fields['discount_type'].widget.attrs.update({'class': 'form-control', 'placeholder': 'discount type'})
        self.fields['discount_amount'].widget.attrs.update({'class': 'form-control', 'placeholder': 'discount amount'})
        self.fields['payment_mode'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Payment Method'})
        self.fields['payment_status'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Payment_status'})
        self.fields['total'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Total Amount payable'})
        self.fields['advance_amount'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Advance Amount'})
        self.fields['vip'].widget.attrs.update({})


