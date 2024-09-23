from django import forms
from .models import *

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'email', 'notes', 'phone', 'address']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
        
        
class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'description', 'purchase_date', 'purchase_price', 'supplier', 'status', 'warranty_period', 'warranty_expiry_date']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'warranty_period': forms.NumberInput(attrs={'class': 'form-control'}),
            'warranty_expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_purchase_price(self):
        price = self.cleaned_data.get('purchase_price')
        if price <= 0:
            raise forms.ValidationError("Purchase price must be positive.")
        return price
    
    
    
class ConsumableItemForm(forms.ModelForm):
    class Meta:
        model = ConsumableItem
        fields = ['name', 'description', 'stock_quantity', 'unit_price', 'total_cost', 'hotel']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'total_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'hotel': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
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
        fields = ['equipment', 'user', 'usage_start_time', 'usage_end_time', 'remarks']
        widgets = {
            'usage_start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'usage_end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'equipment': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
        }


class InsurancePolicyForm(forms.ModelForm):
    class Meta:
        model = InsurancePolicy
        fields = ['equipment', 'policy_number', 'provider', 'coverage_amount', 'start_date', 'expiry_date']
        widgets = {
            'policy_number': forms.TextInput(attrs={'class': 'form-control'}),
            'provider': forms.TextInput(attrs={'class': 'form-control'}),
            'coverage_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'equipment': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_coverage_amount(self):
        amount = self.cleaned_data.get('coverage_amount')
        if amount <= 0:
            raise forms.ValidationError("Coverage amount must be positive.")
        return amount
    
    

class EquipmentAuditLogForm(forms.ModelForm):
    class Meta:
        model = EquipmentAuditLog
        fields = ['equipment', 'changed_by', 'change_description']
        widgets = {
            'change_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'equipment': forms.Select(attrs={'class': 'form-control'}),
            'changed_by': forms.Select(attrs={'class': 'form-control'}),
        }


class InspectionChecklistForm(forms.ModelForm):
    class Meta:
        model = InspectionChecklist
        fields = ['equipment', 'checklist_item', 'is_passed', 'remarks']
        widgets = {
            'checklist_item': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'equipment': forms.Select(attrs={'class': 'form-control'}),
        }