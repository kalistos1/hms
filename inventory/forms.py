from django import forms
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'


class WarehouseForm(forms.ModelForm):

    class Meta:
        model = Warehouse
        fields = ['name',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Warehouse Name',}),
    
        }


class InventoryCategoryForm(forms.ModelForm):

    class Meta:
        model =  ItemCategory
        fields = ['name', 'parent',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Category Name',}),
            'parent': forms.Select(attrs={'class': 'form-control', 'placeholder':'Category Parent If Any',}),
            
        }


class InventoryMovementForm(forms.ModelForm):
    class Meta:
        model = InventoryMovement
        fields = ['item', 'warehouse', 'quantity', 'unit_selling_price', 'movement_type',  'reason']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Choose Item'}),
            'warehouse': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Choose Warehouse'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
            'unit_selling_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter selling price'}),
            'movement_type': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Provide a reason for the movement', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        exclude_types = kwargs.pop('exclude_types', False)
        super(InventoryMovementForm, self).__init__(*args, **kwargs)
        
        # Update widget attributes
        if exclude_types:
            self.fields['movement_type'].choices = [
                (key, value) for key, value in self.fields['movement_type'].choices if key in ['IN', 'OUT']
            ]


class InventoryMovementForm2(forms.ModelForm):
    class Meta:
        model = InventoryMovement
        fields = ['item', 'warehouse', 'quantity', 'unit_selling_price', 'movement_type', 'transfer_location', 'reason']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Choose Item'}),
            'warehouse': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Choose Warehouse'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
            'unit_selling_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter selling price'}),
            'movement_type': forms.Select(attrs={'class': 'form-control'}),
            'transfer_location': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Transfer location (if any)'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Provide a reason for the movement', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        exclude_types = kwargs.pop('exclude_types', False)
        super(InventoryMovementForm2, self).__init__(*args, **kwargs)
        
        # Update movement_type choices to exclude IN, OUT, and ADJUST if exclude_types is True
        if exclude_types:
            self.fields['movement_type'].choices = [
                (key, value) for key, value in self.fields['movement_type'].choices if key not in ['IN', 'OUT', 'ADJUST']
            ]


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
        fields = ['category','item','name', 'code', 'purchase_date',  'status', 'warranty_period', 'warranty_expiry_date','next_service_date',]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control','placeholder':'Equipment Category',}),
            'item': forms.Select(attrs={'class': 'form-control','placeholder':'Item',}),
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Name',}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'rows': 3,'placeholder':'Description',}),
            'status': forms.Select(attrs={'class': 'form-control','placeholder':'Status',}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','placeholder':'Purchase Date',}),
            'warranty_period': forms.NumberInput(attrs={'class': 'form-control','placeholder':'warranty period in years',}),
            'warranty_expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','placeholder':'Warranty Expirey date',}),
            'next_service_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','placeholder':'next service date',}),
        }

    def clean_purchase_price(self):
        price = self.cleaned_data.get('purchase_price')
        if price <= 0:
            raise forms.ValidationError("Purchase price must be positive.")
        return price
    
    
    
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['stock_type','category','name', 'description', 'stock_quantity', 'unit_price', 'purchase_receipt','item_image','supplier','purchase_date','equipment']
        widgets = {
            'stock_type': forms.Select(attrs={'class': 'form-control','placeholder':'Srock type',}),
            'category': forms.Select(attrs={'class': 'form-control','placeholder':'item Category',}),
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Name',}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,'placeholder':'Description',}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Stock Quantity',}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01','placeholder':'Unit Price',}),
            'supplier': forms.Select(attrs={'class': 'form-control','placeholder':'Supplier',}),
            'equipment': forms.Select(attrs={'class': 'form-control', 'type': 'date','placeholder':'Equipment',}),
            'purchase_receipt': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Upload Receipt'}),
            'item_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Upload Receipt'}),
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



class AmenityForm(forms.ModelForm):
    class Meta:
        model = Amenity
        fields = ['name', 'category', 'description', 'cost', 'id_code', 'stock_quantity','supplier']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Name',}),
            'category': forms.Select(attrs={'class': 'form-control', 'type': 'datetime-local','placeholder':'Category',}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'type': 'datetime-local','placeholder':'Usage End Time',}),
            'cost': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Cost Of Use if Any',}),
            'id_code': forms.TextInput(attrs={'class': 'form-control','placeholder':'Order of Usage',}),
            'stock_quantity': forms.TextInput(attrs={'class': 'form-control','placeholder':'Quantity Available if relivant',}),
            'supplier': forms.Select(attrs={'class': 'form-control','placeholder':'Supplier',}),
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