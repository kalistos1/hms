from django.urls import path
from . import views


app_name ="inventory"

urlpatterns = [
    # Supplier URLs
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/create/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/update/', views.supplier_update, name='supplier_update'),
    path('suppliers/<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),

    # categor URLs
    path('categories/', views.category_list, name='category_list'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/<int:pk>/update/', views.category_update, name='category_update'),
    path('category/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # Equipment URLs
    path('equipments/', views.equipment_list, name='equipment_list'),
    path('equipments/create/', views.equipment_create, name='equipment_create'),
    path('equipments/<int:pk>/update/', views.equipment_update, name='equipment_update'),
    path('equipments/<int:pk>/delete/', views.equipment_delete, name='equipment_delete'),

    # Consumable Item URLs
    path('consumable-items/', views.consumable_item_list, name='consumable_item_list'),
    path('consumable-items/create/', views.consumable_item_create, name='consumable_item_create'),
    path('consumable-items/<int:pk>/update/', views.consumable_item_update, name='consumable_item_update'),
    path('consumable-items/<int:pk>/delete/', views.consumable_item_delete, name='consumable_item_delete'),


    # Amenity Item URLs
    path('amenity-items/', views.amenity_item_list, name='amenity_item_list'),
    path('amenity-items/create/', views.amenity_item_create, name='amenity_item_create'),
    path('amenity-items/<int:pk>/update/', views.amenity_item_update, name='amenity_item_update'),
    path('amenity-items/<int:pk>/delete/', views.amenity_item_delete, name='amenity_item_delete'),


    # Equipment Usage Log URLs
    path('usage-logs/', views.equipment_usage_log_list, name='equipment_usage_log_list'),
    path('usage-logs/create/', views.equipment_usage_log_create, name='equipment_usage_log_create'),
    path('usage-logs/<int:pk>/update/', views.equipment_usage_log_update, name='equipment_usage_log_update'),
    path('usage-logs/<int:pk>/delete/', views.equipment_usage_log_delete, name='equipment_usage_log_delete'),

    # Insurance Policy URLs
    path('insurance-policies/', views.insurance_policy_list, name='insurance_policy_list'),
    path('insurance-policies/create/', views.insurance_policy_create, name='insurance_policy_create'),
    path('insurance-policies/<int:pk>/update/', views.insurance_policy_update, name='insurance_policy_update'),
    path('insurance-policies/<int:pk>/delete/', views.insurance_policy_delete, name='insurance_policy_delete'),

    # Equipment Audit Log URLs
    path('audit-logs/', views.equipment_audit_log_list, name='equipment_audit_log_list'),
    path('audit-logs/create/', views.equipment_audit_log_create, name='equipment_audit_log_create'),
    path('audit-logs/<int:pk>/update/', views.equipment_audit_log_update, name='equipment_audit_log_update'),
    path('audit-logs/<int:pk>/delete/', views.equipment_audit_log_delete, name='equipment_audit_log_delete'),

    # Inspection Checklist URLs
    path('checklists/', views.inspection_checklist_list, name='inspection_checklist_list'),
    path('checklists/create/', views.inspection_checklist_create, name='inspection_checklist_create'),
    path('checklists/<int:pk>/update/', views.inspection_checklist_update, name='inspection_checklist_update'),
    path('checklists/<int:pk>/delete/', views.inspection_checklist_delete, name='inspection_checklist_delete'),
]
