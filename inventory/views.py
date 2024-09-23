from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Supplier, Equipment, ConsumableItem, EquipmentUsageLog, InsurancePolicy, EquipmentAuditLog, InspectionChecklist
from .forms import SupplierForm, EquipmentForm, ConsumableItemForm, EquipmentUsageLogForm, InsurancePolicyForm, EquipmentAuditLogForm, InspectionChecklistForm

# Supplier Views
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'suppliers/supplier_list.html', {'suppliers': suppliers})


def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier created successfully.')
            return redirect('supplier_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SupplierForm()
    return render(request, 'suppliers/supplier_form.html', {'form': form})



def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier updated successfully.')
            return redirect('supplier_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'suppliers/supplier_form.html', {'form': form})



def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        messages.success(request, 'Supplier deleted successfully.')
        return redirect('supplier_list')
    return render(request, 'suppliers/supplier_confirm_delete.html', {'supplier': supplier})



# Equipment Views
def equipment_list(request):
    equipments = Equipment.objects.all()
    return render(request, 'equipments/equipment_list.html', {'equipments': equipments})



def equipment_create(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipment created successfully.')
            return redirect('equipment_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EquipmentForm()
    return render(request, 'equipments/equipment_form.html', {'form': form})



def equipment_update(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipment updated successfully.')
            return redirect('equipment_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, 'equipments/equipment_form.html', {'form': form})


def equipment_delete(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        equipment.delete()
        messages.success(request, 'Equipment deleted successfully.')
        return redirect('equipment_list')
    return render(request, 'equipments/equipment_confirm_delete.html', {'equipment': equipment})



# Consumable Item Views
def consumable_item_list(request):
    consumable_items = ConsumableItem.objects.all()
    return render(request, 'consumable_items/consumable_item_list.html', {'consumable_items': consumable_items})



def consumable_item_create(request):
    if request.method == 'POST':
        form = ConsumableItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consumable item created successfully.')
            return redirect('consumable_item_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ConsumableItemForm()
    return render(request, 'consumable_items/consumable_item_form.html', {'form': form})


def consumable_item_update(request, pk):
    consumable_item = get_object_or_404(ConsumableItem, pk=pk)
    if request.method == 'POST':
        form = ConsumableItemForm(request.POST, instance=consumable_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consumable item updated successfully.')
            return redirect('consumable_item_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ConsumableItemForm(instance=consumable_item)
    return render(request, 'consumable_items/consumable_item_form.html', {'form': form})


def consumable_item_delete(request, pk):
    consumable_item = get_object_or_404(ConsumableItem, pk=pk)
    if request.method == 'POST':
        consumable_item.delete()
        messages.success(request, 'Consumable item deleted successfully.')
        return redirect('consumable_item_list')
    return render(request, 'consumable_items/consumable_item_confirm_delete.html', {'consumable_item': consumable_item})



# Equipment Usage Log Views
def equipment_usage_log_list(request):
    usage_logs = EquipmentUsageLog.objects.all()
    return render(request, 'usage_logs/equipment_usage_log_list.html', {'usage_logs': usage_logs})


def equipment_usage_log_create(request):
    if request.method == 'POST':
        form = EquipmentUsageLogForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipment usage log created successfully.')
            return redirect('equipment_usage_log_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EquipmentUsageLogForm()
    return render(request, 'usage_logs/equipment_usage_log_form.html', {'form': form})


def equipment_usage_log_update(request, pk):
    usage_log = get_object_or_404(EquipmentUsageLog, pk=pk)
    if request.method == 'POST':
        form = EquipmentUsageLogForm(request.POST, instance=usage_log)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipment usage log updated successfully.')
            return redirect('equipment_usage_log_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EquipmentUsageLogForm(instance=usage_log)
    return render(request, 'usage_logs/equipment_usage_log_form.html', {'form': form})


def equipment_usage_log_delete(request, pk):
    usage_log = get_object_or_404(EquipmentUsageLog, pk=pk)
    if request.method == 'POST':
        usage_log.delete()
        messages.success(request, 'Equipment usage log deleted successfully.')
        return redirect('equipment_usage_log_list')
    return render(request, 'usage_logs/equipment_usage_log_confirm_delete.html', {'usage_log': usage_log})



# Insurance Policy Views
def insurance_policy_list(request):
    insurance_policies = InsurancePolicy.objects.all()
    return render(request, 'insurance_policies/insurance_policy_list.html', {'insurance_policies': insurance_policies})



def insurance_policy_create(request):
    if request.method == 'POST':
        form = InsurancePolicyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Insurance policy created successfully.')
            return redirect('insurance_policy_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = InsurancePolicyForm()
    return render(request, 'insurance_policies/insurance_policy_form.html', {'form': form})



def insurance_policy_update(request, pk):
    insurance_policy = get_object_or_404(InsurancePolicy, pk=pk)
    if request.method == 'POST':
        form = InsurancePolicyForm(request.POST, instance=insurance_policy)
        if form.is_valid():
            form.save()
            messages.success(request, 'Insurance policy updated successfully.')
            return redirect('insurance_policy_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = InsurancePolicyForm(instance=insurance_policy)
    return render(request, 'insurance_policies/insurance_policy_form.html', {'form': form})



def insurance_policy_delete(request, pk):
    insurance_policy = get_object_or_404(InsurancePolicy, pk=pk)
    if request.method == 'POST':
        insurance_policy.delete()
        messages.success(request, 'Insurance policy deleted successfully.')
        return redirect('insurance_policy_list')
    return render(request, 'insurance_policies/insurance_policy_confirm_delete.html', {'insurance_policy': insurance_policy})


# Equipment Audit Log Views
def equipment_audit_log_list(request):
    audit_logs = EquipmentAuditLog.objects.all()
    return render(request, 'audit_logs/equipment_audit_log_list.html', {'audit_logs': audit_logs})


def equipment_audit_log_create(request):
    if request.method == 'POST':
        form = EquipmentAuditLogForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipment audit log created successfully.')
            return redirect('equipment_audit_log_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EquipmentAuditLogForm()
    return render(request, 'audit_logs/equipment_audit_log_form.html', {'form': form})



def equipment_audit_log_update(request, pk):
    audit_log = get_object_or_404(EquipmentAuditLog, pk=pk)
    if request.method == 'POST':
        form = EquipmentAuditLogForm(request.POST, instance=audit_log)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipment audit log updated successfully.')
            return redirect('equipment_audit_log_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EquipmentAuditLogForm(instance=audit_log)
    return render(request, 'audit_logs/equipment_audit_log_form.html', {'form': form})


def equipment_audit_log_delete(request, pk):
    audit_log = get_object_or_404(EquipmentAuditLog, pk=pk)
    if request.method == 'POST':
        audit_log.delete()
        messages.success(request, 'Equipment audit log deleted successfully.')
        return redirect('equipment_audit_log_list')
    return render(request, 'audit_logs/equipment_audit_log_confirm_delete.html', {'audit_log': audit_log})


# Inspection Checklist Views
def inspection_checklist_list(request):
    checklists = InspectionChecklist.objects.all()
    return render(request, 'checklists/inspection_checklist_list.html', {'checklists': checklists})



def inspection_checklist_create(request):
    if request.method == 'POST':
        form = InspectionChecklistForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inspection checklist created successfully.')
            return redirect('inspection_checklist_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = InspectionChecklistForm()
    return render(request, 'checklists/inspection_checklist_form.html', {'form': form})



def inspection_checklist_update(request, pk):
    checklist = get_object_or_404(InspectionChecklist, pk=pk)
    if request.method == 'POST':
        form = InspectionChecklistForm(request.POST, instance=checklist)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inspection checklist updated successfully.')
            return redirect('inspection_checklist_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = InspectionChecklistForm(instance=checklist)
    return render(request, 'checklists/inspection_checklist_form.html', {'form': form})



def inspection_checklist_delete(request, pk):
    checklist = get_object_or_404(InspectionChecklist, pk=pk)
    if request.method == 'POST':
        checklist.delete()
        messages.success(request, 'Inspection checklist deleted successfully.')
        return redirect('inspection_checklist_list')
    return render(request, 'checklists/inspection_checklist_confirm_delete.html', {'checklist': checklist})
