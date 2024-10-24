from django.shortcuts import render
from .models import PaymentRecord
from .forms import PaymentReportForm
from django.utils.timezone import make_aware
from datetime import datetime
from inventory.models import Item, Equipment
from .forms import PurchaseReportForm
from django.db.models import Sum,Count
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string




def booking_payments_list(request):
    booking_payments = PaymentRecord.objects.filter(source='booking').order_by('-payment_date')
    context = {
        'booking_payments': booking_payments,
    }
    return render(request, 'account_officer/booking_payment_list.html', context)



def pos_payments_list(request):
    pos_payments = PaymentRecord.objects.filter(source='pos').order_by('-payment_date')
    context = {
        'pos_payments': pos_payments,
    }
    return render(request, 'account_officer/pos_payment_list.html', context)



def payment_report_view(request):
    form = PaymentReportForm(request.GET or None)  # Bind GET parameters to the form
    payment_records = PaymentRecord.objects.none()  # Default empty queryset

    if form.is_valid():
        # Get the start and end dates
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')

        # Convert to aware datetime objects if necessary (to handle timezone issues)
        start_datetime = make_aware(datetime.combine(start_date, datetime.min.time()))
        end_datetime = make_aware(datetime.combine(end_date, datetime.max.time()))

        # Filter by date range
        payment_records = PaymentRecord.objects.filter(payment_date__range=(start_datetime, end_datetime))

        # Filter by source if one is selected
        source = form.cleaned_data.get('source')
        if source:
            payment_records = payment_records.filter(source=source)

    context = {
        'form': form,
        'payment_records': payment_records,
    }

    # If the request is an HTMX request, return only the snippet
    if request.headers.get('HX-Request'):
        if not payment_records.exists():
            context['error_message'] = "No payment records found for the selected dates and source."
        return render(request, 'partials/htmx/payment_report_snippet.html', context)

    # Otherwise, render the full page
    return render(request, 'account_officer/booking_pos_report.html', context)


def purchase_report(request):
    form = PurchaseReportForm()
    report_data = None
    total_purchase_value = 0
    total_number_of_purchases = 0
    supplier_payments_summary = None
    start_date = None
    end_date = None
    error_message = None

    if request.method == 'POST':
        form = PurchaseReportForm(request.POST)
        
        if form.is_valid():
            report_type = form.cleaned_data['report_type']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            if report_type == 'consumables':
                report_data = Item.objects.filter(
                    purchase_date__range=[start_date, end_date]
                ).values(
                    'name', 'description', 'stock_quantity', 'unit_price', 'unit_price', 
                    'purchase_date', 'category__name', 'supplier__name', 'supplier__contact_person', 
                    'supplier__email', 'supplier__phone', 'supplier__address', 
                ).annotate(
                    all_total_cost=Sum('unit_price')
                )

            elif report_type == 'equipment':
                report_data = Equipment.objects.filter(
                    purchase_date__range=[start_date, end_date]
                ).values(
                    'name', 'category', 'code', 'item__description', 'item__unit_price', 'purchase_date', 'status', 
                    'warranty_period', 'warranty_expiry_date', 'next_service_date', 
                    'item__supplier__name', 'item__supplier__contact_person', 'item__supplier__email', 
                    'item__supplier__phone', 'item__supplier__address', 'category__name'
                ).annotate(
                    total_price=Sum('item__unit_price')
                )

            if report_data.exists():
                total_purchase_value = report_data.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
                total_number_of_purchases = report_data.count()

                # Supplier payments summary
                supplier_payments_summary = report_data.values(
                    'supplier__name'
                ).annotate(
                    total_paid=Sum('total_cost')
                ).order_by('-total_paid')
            else:
                error_message = "No records found for the selected date range and report type."

        else:
            error_message = "Invalid form submission. Please correct the errors."

    context = {
        'form': form,
        'report_data': report_data,
        'start_date': start_date,
        'end_date': end_date,
        'total_purchase_value': total_purchase_value,
        'total_number_of_purchases': total_number_of_purchases,
        'supplier_payments_summary': supplier_payments_summary,
        'error_message': error_message,
    }

    # Handle HTMX request to load only the report part
    if request.headers.get('HX-Request'):
        if not report_data:
            context['error_message'] = "No purchase records found for the selected date range and report type."
        return render(request, 'partials/htmx/purchase_report.html', context)

    return render(request, 'account_officer/purchasing_report.html', context)

