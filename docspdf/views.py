from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML, CSS
from pathlib import Path
import logging

from .forms import QuotationForm, QuotationItemForm, InvoiceForm, InvoiceItemForm
from .models import Quotation, QuotationItem, Invoice, InvoiceItem
from core.models import CompanyProfile

logger = logging.getLogger(__name__)

# ----------------------------
# Invoice 関連のビュー
# ----------------------------

@login_required
def create_invoice(request):
    InvoiceItemFormSet = modelformset_factory(InvoiceItem, form=InvoiceItemForm, extra=1, can_delete=True)
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST, queryset=InvoiceItem.objects.none())

        if not form.is_valid():
            logger.error(f"InvoiceForm エラー: {form.errors}")
        if not formset.is_valid():
            logger.error(f"InvoiceItemFormSet エラー: {formset.errors}")

        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.creator = request.user
            invoice.save()
            for form_item in formset:
                item = form_item.save(commit=False)
                item.invoice = invoice
                item.subtotal = item.quantity * item.unit_price
                item.save()
            return redirect('invoice_confirm', pk=invoice.pk)
        else:
            return render(request, 'docspdf/create_invoice.html', {
                'form': form,
                'formset': formset,
                'form_errors': form.errors,
                'formset_errors': formset.errors,
            })
    else:
        form = InvoiceForm()
        formset = InvoiceItemFormSet(queryset=InvoiceItem.objects.none())

    return render(request, 'docspdf/create_invoice.html', {
        'form': form,
        'formset': formset,
    })

@login_required
def invoice_list(request):
    invoices = Invoice.objects.all().order_by('-created_at')
    return render(request, 'docspdf/invoice_list.html', {'invoices': invoices})

@login_required
def invoice_confirm(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    items = list(InvoiceItem.objects.filter(invoice=invoice))
    while len(items) < 15:
        items.append(None)
    total_amount = sum(item.subtotal for item in items if item)
    tax_amount = int(total_amount * 0.1)
    total_with_tax = total_amount + tax_amount
    company = CompanyProfile.objects.first()

    return render(request, 'docspdf/invoice_confirm.html', {
        'invoice': invoice,
        'items': items,
        'total_amount': total_amount,
        'tax_amount': tax_amount,
        'total_with_tax': total_with_tax,
        'company': company,
    })

@login_required
def edit_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    InvoiceItemFormSet = modelformset_factory(InvoiceItem, form=InvoiceItemForm, extra=0, can_delete=True)

    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        formset = InvoiceItemFormSet(request.POST, queryset=InvoiceItem.objects.filter(invoice=invoice))
        if form.is_valid() and formset.is_valid():
            invoice = form.save()
            items = formset.save(commit=False)
            for item in items:
                item.invoice = invoice
                item.subtotal = item.quantity * item.unit_price
                item.save()
            for item in formset.deleted_objects:
                item.delete()
            return redirect('invoice_confirm', pk=invoice.pk)
        else:
            logger.error(f"Form errors: {form.errors}")
            logger.error(f"Formset errors: {formset.errors}")
    else:
        form = InvoiceForm(instance=invoice)
        formset = InvoiceItemFormSet(queryset=InvoiceItem.objects.filter(invoice=invoice))

    return render(request, 'docspdf/edit_invoice.html', {
        'form': form,
        'formset': formset,
    })

@login_required
def invoice_preview(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    items = InvoiceItem.objects.filter(invoice=invoice)
    company = CompanyProfile.objects.first()

    total_amount = sum(item.subtotal for item in items)
    tax_amount = int(total_amount * 0.1)
    total_with_tax = total_amount + tax_amount

    html_string = render_to_string('docspdf/invoice_pdf.html', {
        'invoice': invoice,
        'items': items,
        'total_amount': total_amount,
        'tax_amount': tax_amount,
        'total_with_tax': total_with_tax,
        'company': company,
        'user': request.user,
    })

    return HttpResponse(html_string)

@login_required
def invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    items = list(InvoiceItem.objects.filter(invoice=invoice))
    while len(items) < 15:
        items.append(None)
    company = CompanyProfile.objects.first()
    total_amount = sum(item.subtotal for item in items if item)
    tax_amount = int(total_amount * 0.1)
    total_with_tax = total_amount + tax_amount

    html_string = render_to_string('docspdf/invoice_pdf.html', {
        'invoice': invoice,
        'items': items,
        'total_amount': total_amount,
        'tax_amount': tax_amount,
        'total_with_tax': total_with_tax,
        'company': company,
        'user': request.user,
    })

    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    css_path = Path(settings.BASE_DIR) / "static" / "css" / "pdf_style.css"
    css = CSS(filename=str(css_path.resolve()))

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'
    html.write_pdf(response, stylesheets=[css])
    return response

# ----------------------------
# Quotation 関連のビュー
# ----------------------------

@login_required
def create_quotation(request):
    QuotationItemFormSet = modelformset_factory(QuotationItem, form=QuotationItemForm, extra=1, can_delete=True)
    if request.method == 'POST':
        form = QuotationForm(request.POST)
        formset = QuotationItemFormSet(request.POST, queryset=QuotationItem.objects.none())
        if form.is_valid() and formset.is_valid():
            quotation = form.save(commit=False)
            quotation.creator = request.user
            quotation.save()
            for form_item in formset:
                item = form_item.save(commit=False)
                item.quotation = quotation
                item.subtotal = item.quantity * item.unit_price
                item.save()
            return redirect('quotation_confirm', pk=quotation.pk)
        else:
            return render(request, 'docspdf/create_quotation.html', {
                'form': form,
                'formset': formset,
                'form_errors': form.errors,
                'formset_errors': formset.errors,
            })
    else:
        form = QuotationForm()
        formset = QuotationItemFormSet(queryset=QuotationItem.objects.none())

    return render(request, 'docspdf/create_quotation.html', {
        'form': form,
        'formset': formset,
    })

@login_required
def quotation_list(request):
    quotations = Quotation.objects.all().order_by('-created_at')
    return render(request, 'docspdf/quotation_list.html', {'quotations': quotations})

@login_required
def quotation_confirm(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    items = list(QuotationItem.objects.filter(quotation=quotation))
    while len(items) < 15:
        items.append(None)
    total_amount = sum(item.subtotal for item in items if item)
    tax_amount = int(total_amount * 0.1)
    total_with_tax = total_amount + tax_amount
    company = CompanyProfile.objects.first()

    return render(request, 'docspdf/quotation_confirm.html', {
        'quotation': quotation,
        'items': items,
        'total_amount': total_amount,
        'tax_amount': tax_amount,
        'total_with_tax': total_with_tax,
        'company': company,
        'user': request.user,
    })

@login_required
def edit_quotation(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    QuotationItemFormSet = modelformset_factory(QuotationItem, form=QuotationItemForm, extra=0, can_delete=True)

    if request.method == 'POST':
        form = QuotationForm(request.POST, instance=quotation)
        formset = QuotationItemFormSet(request.POST, queryset=QuotationItem.objects.filter(quotation=quotation))
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('quotation_confirm', pk=quotation.pk)
    else:
        form = QuotationForm(instance=quotation)
        formset = QuotationItemFormSet(queryset=QuotationItem.objects.filter(quotation=quotation))

    return render(request, 'docspdf/edit_quotation.html', {
        'form': form,
        'formset': formset,
    })

@login_required
def quotation_pdf(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    items = list(QuotationItem.objects.filter(quotation=quotation))
    while len(items) < 15:
        items.append(None)
    company = CompanyProfile.objects.first()
    total_amount = sum(item.subtotal for item in items if item)
    tax_amount = int(total_amount * 0.1)
    total_with_tax = total_amount + tax_amount

    html_string = render_to_string('docspdf/quotation_pdf.html', {
        'quotation': quotation,
        'items': items,
        'total_amount': total_amount,
        'tax_amount': tax_amount,
        'total_with_tax': total_with_tax,
        'company': company,
    })

    css_path = Path(settings.STATICFILES_DIRS[0]) / "css" / "style.css"
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    css = CSS(filename=str(css_path.resolve()))

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="quotation_{quotation.quotation_number}.pdf"'
    html.write_pdf(response, stylesheets=[css])
    return response