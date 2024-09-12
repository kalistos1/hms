from django import forms
from bookings.models import *
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
    pass
    # class Meta:
    #     model = Booking
    #     fields = [
    #         'room_type', 'room', 'check_in_date', 'check_out_date', 
    #         'num_adults', 'num_children',
    #         'total',  
           
    #     ]

    #     room = forms.ModelMultipleChoiceField(
    #         queryset=Room.objects.filter(is_available=True), 
    #         required=True,
    #         widget=forms.CheckboxSelectMultiple,  
    #     )

    # def __init__(self, *args, **kwargs):
    #     super(BookingForm, self).__init__(*args, **kwargs)
        
       
    #     available_rooms = Room.objects.filter(
    #         is_available=True
    #     ).exclude(
    #         id__in=Booking.objects.filter(is_active=False).values_list('room__id', flat=True)
    #     )
    #     self.fields['room'].queryset = available_rooms
        
    #     # Check if there are any available rooms
    #     if not available_rooms.exists():
    #         self.fields['room'].widget.attrs['placeholder'] = 'No available room'
    #         self.fields['room'].widget = forms.TextInput(attrs={
    #             'class': 'form-control', 
    #             'placeholder': 'No available room'
    #         })
    #     else:
    #         self.fields['room'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Room'})
        
    #     self.fields['check_in_date'].widget = DateInput(attrs={'class': 'form-control','placeholder': 'Check-In Date'})
    #     self.fields['check_out_date'].widget = DateInput(attrs={'class': 'form-control','placeholder': 'Check-Out Date'})
    #     self.fields['booking_type'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Booking Type'})
    #     self.fields['arrival_from'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Arrival From'})
    #     self.fields['room_type'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Room Type'})
    #     self.fields['num_adults'].widget.attrs.update({'class': 'form-control', 'placeholder': 'No. Adults'})
    #     self.fields['num_children'].widget.attrs.update({'class': 'form-control', 'placeholder': 'No. Children'})
    #     self.fields['discount_type'].widget.attrs.update({'class': 'form-control', 'placeholder': 'discount type'})
    #     self.fields['discount_amount'].widget.attrs.update({'class': 'form-control', 'placeholder': 'discount amount'})
    #     self.fields['payment_mode'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Payment Method'})
    #     self.fields['payment_status'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Payment_status'})
    #     self.fields['total'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Total Amount payable'})
    #     self.fields['advance_amount'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Advance Amount'})
    #     self.fields['vip'].widget.attrs.update({})
        
        
class RoomAmenityForm(forms.ModelForm):
    class Meta:
        model = RoomAmenity
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RoomAmenityForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Amenity Name'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Description'})
        
        


class RoomTypeForm(forms.ModelForm):
    
    class Meta:
        model = RoomType
        fields = ['banner_img','type','base_price', 'number_of_beds', 'room_capacity',]

    def __init__(self, *args, **kwargs):
        super(RoomTypeForm, self).__init__(*args, **kwargs)
      
        self.fields['banner_img'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['type'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Room Type'})
        self.fields['base_price'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Price'})
        self.fields['number_of_beds'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Number of Beds'})
        self.fields['room_capacity'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Room Capacity'})
         
        
        

class RoomForm(forms.ModelForm):
 
    class Meta:
        model = Room
        fields = ['room_type','banner_img','room_number','floor','amenities',]

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
     
        self.fields['room_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['banner_img'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['room_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Room Number'})
        self.fields['floor'].widget.attrs.update({'class': 'form-control'})
        self.fields['amenities'].widget.attrs.update({'class': 'form-control'})
       



class RoomServicesForm(forms.ModelForm):
    class Meta:
        model = RoomServices
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RoomServicesForm, self).__init__(*args, **kwargs)
        self.fields['booking'].widget.attrs.update({'class': 'form-control'})
        self.fields['room'].widget.attrs.update({'class': 'form-control'})
        self.fields['service_type'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Service Type'})
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Price'})
        
        
        
        
class CreateCouponForm(forms.ModelForm):
 
    class Meta:
        model = Coupon
        fields =[ 'code', 'type','discount','redemption','active', 'valid_from', 'valid_to']
        
    def __init__(self, *args, **kwargs):
        super(CreateCouponForm, self).__init__(*args, **kwargs)
        self.fields['code'].widget.attrs.update({'class': 'form-control', 'placeholder': 'coupon code'})
        self.fields['type'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Coupon Type'})
        self.fields['discount'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Discount value'})
        self.fields['redemption'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Redemption'})  
        self.fields['active'].widget.attrs.update({})      
        self.fields['valid_from'].widget= DateInput(attrs={'class': 'form-control','placeholder': 'Valid From'}) 
        self.fields['valid_to'].widget=DateInput(attrs={'class': 'form-control','placeholder': 'Valid To'}) 

