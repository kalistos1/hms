from django import forms
from django.utils import timezone
from .models import POSUser, PosStockReceipt
from hrm.models import StaffSchedules, Attendance
from django.db.models import Q

class WaiterCheckoutForm(forms.Form):
    waiter = forms.ModelChoiceField(
        queryset=POSUser.objects.none(),  # Placeholder, will be populated dynamically in the view
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Assigned Waiter"
    )

    def __init__(self, *args, department_location=None, **kwargs):
        super().__init__(*args, **kwargs)

        if department_location:
            now = timezone.now().date()  # Current date

            # Fetch both POS users and waiters linked to the department location
            pos_users = POSUser.objects.filter(
                Q(employee__department_location=department_location) | 
                Q(waiter__department_location=department_location)
            ).distinct()

            # Initialize valid users who have schedules and attendance records
            valid_pos_users = []
            valid_waiters = []
            for pos_user in pos_users:
                # POS Users
                employee = pos_user.employee
                if self.is_valid_user(employee, now):
                    valid_pos_users.append(pos_user.pk)

                # Waiters (linked through `waiter` ForeignKey)
                waiter = pos_user.waiter
                if waiter and self.is_valid_user(waiter, now):
                    valid_waiters.append(pos_user.pk)

            # Set the queryset to include both POS users and waiters who meet the criteria
            self.fields['waiter'].queryset = POSUser.objects.filter(
                Q(pk__in=valid_pos_users) | Q(pk__in=valid_waiters)
            )

    def is_valid_user(self, employee, date):
        """Helper function to check if an employee has a valid schedule and attendance."""
        # Check if employee has an active schedule today for POS or Waiter shifts
        schedule_exists = StaffSchedules.objects.filter(
            employee=employee,
            schedule_type__in=['Pos_shift', 'Waiter_shift'],
            schedule_start_date__lte=date,
            schedule_end_date__gte=date,
            active=True
        ).exists()

        # Check if employee has an active attendance record today
        attendance_exists = Attendance.objects.filter(
            employee=employee,
            active=True,
            check_in__date=date
        ).exists()

        return schedule_exists and attendance_exists


class updateReceivedItemForm(forms.ModelForm):
    
    class Meta:
        model =  PosStockReceipt
        fields = ("product","quantity_received")

    def __init__(self, *args, **kwargs):
        super( updateReceivedItemForm, self).__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Choose Product'})
        self.fields['quantity_received'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Quantity Received'})
      