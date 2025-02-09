# customers/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer
from .forms import CustomerForm, CustomerCSVImportForm
from django.http import HttpResponse
import csv

def customer_list(request):
    query = request.GET.get('q', '')
    customers = Customer.objects.all()
    if query:
        customers = customers.filter(
            first_name__icontains=query
        ) | customers.filter(
            last_name__icontains=query
        ) | customers.filter(
            email__icontains=query
        )
    return render(request, 'customers/customer_list.html', {'customers': customers, 'query': query})

def add_or_edit_customer(request, customer_id=None):
    if customer_id:
        customer = get_object_or_404(Customer, id=customer_id)
    else:
        customer = None

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customers/customer_form.html', {'form': form})

def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer.delete()
    return redirect('customer_list')

def export_customers_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"'

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Email', 'Phone Number', 'Company Name', 'Address'])

    for customer in Customer.objects.all():
        writer.writerow([
            customer.first_name,
            customer.last_name,
            customer.email,
            customer.phone_number,
            customer.company_name,
            customer.address
        ])

    return response

def import_customers_csv(request):
    if request.method == "POST":
        form = CustomerCSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            preview_data = []
            errors = []

            # データをプレビュー用に処理
            for row in reader:
                try:
                    preview_data.append({
                        "first_name": row.get('First Name', ''),
                        "last_name": row.get('Last Name', ''),
                        "email": row.get('Email', ''),
                        "phone_number": row.get('Phone Number', ''),
                        "company_name": row.get('Company Name', ''),
                        "address": row.get('Address', ''),
                    })
                except Exception as e:
                    errors.append(f"エラー: {row} - {e}")

            # プレビュー画面へ
            if not errors:
                request.session['preview_data'] = preview_data  # セッションに保存
                return redirect('confirm_import')

            return render(request, "customers/import_customers.html", {"form": form, "errors": errors})
    else:
        form = CustomerCSVImportForm()

    return render(request, "customers/import_customers.html", {"form": form})


def confirm_import(request):
    preview_data = request.session.get('preview_data', [])
    if request.method == "POST":
        for row in preview_data:
            Customer.objects.create(
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email'],
                phone_number=row['phone_number'],
                company_name=row['company_name'],
                address=row['address'],
            )
        del request.session['preview_data']  # セッションデータを削除
        return redirect('customer_list')

    return render(request, "customers/confirm_import.html", {"preview_data": preview_data})

import logging
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer
from .forms import CustomerForm

logger = logging.getLogger('django')

def add_or_edit_customer(request, customer_id=None):
    """
    顧客情報の追加・編集
    """
    customer = get_object_or_404(Customer, id=customer_id) if customer_id else None
    original_data = {}

    if customer_id:
        # 保存前のデータをコピー
        for field in ['first_name', 'last_name', 'email', 'phone_number', 'company_name', 'address']:
            original_data[field] = getattr(customer, field, None)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            instance = form.save(commit=False)
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if customer_id:  # 編集時
                changes = []
                for field in original_data:
                    old_value = original_data[field]
                    new_value = getattr(instance, field, None)
                    if str(old_value) != str(new_value):  # 文字列として比較
                        changes.append(f"{field} from '{old_value}' to '{new_value}'")
                if changes:
                    logger.info(f"[{current_time}] User: {request.user.username} updated Customer ID={customer.id} - Changes: {', '.join(changes)}")
                else:
                    logger.info(f"[{current_time}] User: {request.user.username} updated Customer ID={customer.id} - No changes made")
            else:  # 新規作成
                logger.info(f"[{current_time}] User: {request.user.username} created Customer ID=NEW - Name: {instance.first_name} {instance.last_name}")
            
            instance.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customers/edit_customer.html', {'form': form})


def delete_customer(request, customer_id):
    """
    顧客情報の削除
    """
    customer = get_object_or_404(Customer, id=customer_id)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info(f"[{current_time}] User: {request.user.username} deleted Customer ID={customer.id} - Name: {customer.first_name} {customer.last_name}")
    customer.delete()
    return redirect('customer_list')
