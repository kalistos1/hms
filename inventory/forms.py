from django import forms
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class InventoryCategoryForm(forms.ModelForm):

    class Meta:
        model =  ItemCategory
        fields = ['name', 'parent',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Category Name',}),
            'parent': forms.Select(attrs={'class': 'form-control', 'placeholder':'Category Parent If Any',}),
            
        }
        

class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'email', 'notes', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Suppliers name',}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'suppliers Email',}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Suppliers Phone',}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder':'suppliers Address',}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Contact Persons Number',}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'additional information', 'rows': 2}),
        }
        

   
        
class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['category','name', 'description', 'purchase_date', 'purchase_price', 'supplier','purchase_receipt', 'status', 'warranty_period', 'warranty_expiry_date']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control','placeholder':'Equipment Category',}),
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Name',}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,'placeholder':'Description',}),
            'supplier': forms.Select(attrs={'class': 'form-control','placeholder':'Supplier',}),
            'status': forms.Select(attrs={'class': 'form-control','placeholder':'Status',}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','placeholder':'Purchase Date',}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01','placeholder':'Purchase price',}),
            'purchase_receipt': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Upload Receipt'}),
            'warranty_period': forms.NumberInput(attrs={'class': 'form-control','placeholder':'warranty period in years',}),
            'warranty_expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','placeholder':'Warranty Expirey date',}),
           
        }

    def clean_purchase_price(self):
        price = self.cleaned_data.get('purchase_price')
        if price <= 0:
            raise forms.ValidationError("Purchase price must be positive.")
        return price
    
    
    
class ConsumableItemForm(forms.ModelForm):
    class Meta:
        model = ConsumableItem
        fields = ['category','name', 'description', 'stock_quantity', 'unit_price', 'purchase_receipt', 'purchase_date']
        widgets = {
            
            'category': forms.Select(attrs={'class': 'form-control','placeholder':'item Category',}),
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Name',}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,'placeholder':'Description',}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Stock Quantity',}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01','placeholder':'Unit Price',}),
            'purchase_receipt': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Upload Receipt'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','placeholder':'Purchase Date',}),
         
        }

    def clean_unit_price(self):
        price = self.cleaned_data.get('unit_price')
        if price <= 0:
            raise forms.ValidationError("Unit price must be positive.")
        return price

    def clean_total_cost(self):
        cost = self.cleaned_data.get('total_cost')
        if cost < 0:
            raise forms.ValidationError("Total cost cannot be negative.")
        return cost
    
    

class EquipmentUsageLogForm(forms.ModelForm):
    class Meta:
        model = EquipmentUsageLog
        fields = ['equipment', 'usage_start_time', 'usage_end_time', 'remarks']
        widgets = {
             'equipment': forms.Select(attrs={'class': 'form-control','placeholder':'Equipment',}),
            'usage_start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local','placeholder':'Usage Start Time',}),
            'usage_end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local','placeholder':'Usage End Time',}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2,'placeholder':'Additional Remark',}),
           
           
        }


class InsurancePolicyForm(forms.ModelForm):
    class Meta:
        model = InsurancePolicy
        fields = ['equipment', 'policy_number', 'provider', 'coverage_amount', 'start_date', 'expiry_date']
        widgets = {
            'equipment': forms.Select(attrs={'class': 'form-control','placeholder':'Insured Equipment',}),
            'policy_number': forms.TextInput(attrs={'class': 'form-control','placeholder':'Policy Number',}),
            'provider': forms.TextInput(attrs={'class': 'form-control','placeholder':'Insurance provider',}),
            'coverage_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01','placeholder':'Coverage Amount',}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','placeholder':'Insurance Start Date',}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','placeholder':'Insurance Expiry Date',}),
           
        }

    def clean_coverage_amount(self):
        amount = self.cleaned_data.get('coverage_amount')
        if amount <= 0:
            raise forms.ValidationError("Coverage amount must be positive.")
        return amount
    
    

class EquipmentAuditLogForm(forms.ModelForm):
    class Meta:
        model = EquipmentAuditLog
        fields = ['equipment', 'change_description']
        widgets = {
            'change_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,'placeholder':'description',}),
            'equipment': forms.Select(attrs={'class': 'form-control','placeholder':'Equipment',}),
            
        }


class InspectionChecklistForm(forms.ModelForm):
    class Meta:
        model = InspectionChecklist
        fields = ['inspector','equipment', 'checklist_item', 'is_passed', 'remarks']
        widgets = {
            'inspector': forms.TextInput(attrs={'class': 'form-control'}),
            'equipment': forms.Select(attrs={'class': 'form-control'}),
            'checklist_item': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
           
        }