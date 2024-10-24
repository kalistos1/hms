from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import *
from .forms import *
# Supplier Views
def supplier_list(request):
    suppliers = Supplier.objects.all()
    form = SupplierForm()
    context =  {
        'suppliers': suppliers,
        'form':form
        }
    return render(request, 'pages/supplier_list.html',context)


def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier created successfully.')
            return redirect('inventory:supplier_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
       messages.error(request,"something went wrong, check the form and try again")
    return redirect('inventory:supplier_list')



def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier updated successfully.')
            return redirect('inventory:supplier_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'suppliers/supplier_form.html', {'form': form})



def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'GET':
        supplier.delete()
        messages.success(request, 'Supplier deleted successfully.')
        return redirect('inventory:supplier_list')
    else:
        messages.error(request,' something went wrong, Unable to delete supplier')
    return redirect('inventory:supplier_list')



# Category Views
def category_list(request):
    categories = ItemCategory.objects.all()
    form =  InventoryCategoryForm()
    context =  {
        'categories': categories,
        'form':form
        }
    return render(request, 'pages/item_category.html',context)


def category_create(request):
    if request.method == 'POST':
        form = InventoryCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully.')
            return redirect('inventory:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
       messages.error(request,"something went wrong, check the form and try again")
    return redirect('inventory:category_list')



def category_update(request, pk):
    category = get_object_or_404(ItemCategory, pk=pk)
    if request.method == 'POST':
        form = InventoryCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('inventory:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SupplierForm(instance=category)
    return render(request, 'suppliers/supplier_form.html', {'form': form})



def category_delete(request, pk):
    category = get_object_or_404(ItemCategory, pk=pk)
    if request.method == 'GET':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('inventory:category_list')
    else:
        messages.error(request,' something went wrong, Unable to delete supplier')
    return redirect('inventory:category_list')



# Equipment Views
def equipment_list(request):
    equipments = Equipment.objects.all()
    form = EquipmentForm()
    context =  {
        'equipments': equipments,
        'form':form,
        }
    return render(request, 'pages/equipment_list.html',context)



def equipment_create(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipment created successfully.')
            return redirect('inventory:equipment_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        messages.error(request, 'Something went Wrong Unable to Add Equipment.')
    return  redirect('inventory:equipment_list')



def equipment_update(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipment updated successfully.')
            return redirect('inventory:equipment_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, 'equipments/equipment_form.html', {'form': form})


def equipment_delete(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'GET':
        equipment.delete()
        messages.success(request, 'Equipment deleted successfully.')
        return redirect('inventory:equipment_list')
    return redirect('inventory:equipment_list')



# Consumable Item Views
def consumable_item_list(request):
    consumable_items = Item.objects.all()
    form = ItemForm()
    context = {
        'consumable_items': consumable_items,
        'form':form,
        }

    return render(request, 'pages/consumable_item_list.html', context)


def consumable_item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consumable item created successfully.')
            return redirect('inventory:consumable_item_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        messages.error(request, 'Something went wrong check form and resubmit')
    return redirect ('inventory:consumable_item_list')


def consumable_item_update(request, pk):
    consumable_item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=consumable_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consumable item updated successfully.')
            return redirect('inventory:consumable_item_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ItemForm(instance=consumable_item)
    return render(request, 'pages/consumable_item_form.html', {'form': form})


def consumable_item_delete(request, pk):
    consumable_item = get_object_or_404(Item, pk=pk)
    if request.method == 'GET':
        consumable_item.delete()
        messages.success(request, 'Consumable item deleted successfully.')
        return redirect('inventory:consumable_item_list')
    messages.error(request, 'Unable to delete item something went wrong.')
    return redirect('inventory:consumable_item_list')


# Amenity Item Views
def amenity_item_list(request):
    amenities = Amenity.objects.all()
    form = AmenityForm()
    context = {
        'amenities': amenities,
        'form':form,
        }

    return render(request, 'pages/amenity_list.html', context)


def amenity_item_create(request):
    if request.method == 'POST':
        form = AmenityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Amenity created successfully.')
            return redirect('inventory:amenity_item_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        messages.error(request, 'Something went wrong check form and resubmit')
    return redirect ('inventory:amenity_item_list')


def amenity_item_update(request, pk):
    amenity = get_object_or_404(Amenity, pk=pk)
    if request.method == 'POST':
        form = AmenityForm(request.POST, instance=amenity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Amenity updated successfully.')
            return redirect('inventory:amenity_item_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ConsumableItemForm(instance=amenity)
    return render(request, 'pages/amenity_item_form.html', {'form': form})


def amenity_item_delete(request, pk):
    amenity = get_object_or_404(Amenity, pk=pk)
    if request.method == 'GET':
        amenity.delete()
        messages.success(request, 'amnenity deleted successfully.')
        return redirect('inventory:amenity_item_list')
    messages.error(request, 'Unable to delete item something went wrong.')
    return redirect('inventory:amenity_item_list')


def move_product(request):
    if request.method  == "POST":
        form =  InventoryMovementForm(request.POST)
        warehouse = Warehouse.objects.first()
        employee = get_object_or_404(Employee, user=request.user)

        if form.is_valid:
           move_data = form.save(commit=False)
           move_data.warehouse = warehouse
           move_data.performed_by = employee
           move_data.save()

           messages.success(request, 'item Moved Succesful')
           return redirect('inventory:warehouse_stock')
        else:
            messages.error(request,'Something happened, item was not moved')
            return redirect('dashboard:warehouse_info')
    else:
        messages.error(request,'Something happened, item was not moved')
        return redirect('dashboard:warehouse_info')


    


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



def supervisor_reports(request):
    return render(request,'supervisor/reports.html')
