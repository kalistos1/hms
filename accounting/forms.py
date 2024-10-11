from django import forms
from .models import PaymentRecord

class PaymentReportForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),  # Bootstrap class
        required=True
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),  # Bootstrap class
        required=True
    )
    
    # Choices for the source field, using the choices from the model
    source = forms.ChoiceField(
        choices=[('', 'All')] + PaymentRecord.PAYMENT_SOURCE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})  # Bootstrap class for select dropdown
    )



class PurchaseReportForm(forms.Form):
    REPORT_CHOICES = (
        ('', 'Choose Report'),
        ('consumables', 'Consumables'),
        ('equipment', 'Equipment'),
    )
    
    # Add Bootstrap classes to the fields using the 'widget' attribute
    report_type = forms.ChoiceField(
        choices=REPORT_CHOICES,
        label="Report Type",
        widget=forms.Select(attrs={
            'class': 'form-control'  # Bootstrap form control class for select dropdown
        })
    )
    
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',  # Bootstrap form control class for date input
            'type': 'date'            # HTML5 date input
        }),
        label="Start Date"
    )
    
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',  # Bootstrap form control class for date input
            'type': 'date'            # HTML5 date input
        }),
        label="End Date"
    )