from django import forms
from bookings.models import *
from accounts.models import  User, Profile
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class DateInput(forms.DateInput):
    input_type = 'date'

 
        
class RoomAmenityForm(forms.ModelForm):
    class Meta:
        model =  RoomInventory
        fields = ['room','equipment','amenity','consumable','quantity','status']
    

    def __init__(self, *args, **kwargs):
        super(RoomAmenityForm, self).__init__(*args, **kwargs)
       
        self.fields['room'].widget.attrs.update({'class': 'form-control', 'placeholder': 'room'})
        self.fields['equipment'].widget.attrs.update({'class': 'form-control', 'placeholder': 'equipment'})
        self.fields['amenity'].widget.attrs.update({'class': 'form-control', 'placeholder': 'amenity'})
        self.fields['consumable'].widget.attrs.update({'class': 'form-control', 'placeholder': 'consumable'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control', 'placeholder': 'quantity'})
        self.fields['status'].widget.attrs.update({'class': 'form-control', 'placeholder': 'status'})
        
    
        
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
        fields = ['room_type','banner_img','room_number','floor',]

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
     
        self.fields['room_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['banner_img'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['room_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Room Number'})
        self.fields['floor'].widget.attrs.update({'class': 'form-control'})
      
       
                
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

