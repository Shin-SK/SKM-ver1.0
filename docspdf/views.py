from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Sum
from django.conf import settings
import os
from weasyprint import HTML, CSS
import logging
from .forms import QuotationForm, QuotationItemForm, InvoiceForm, InvoiceItemForm
from .models import Quotation, QuotationItem, Invoice, InvoiceItem
from core.models import CompanyProfile  # 会社情報をインポート

# ログを有効化
logger = logging.getLogger(__name__)

@login_required
def create_invoice(request):
    InvoiceItemFormSet = modelformset_factory(InvoiceItem, form=InvoiceItemForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST, queryset=InvoiceItem.objects.none())

        # **デバッグ用のログを追加**
        if not form.is_valid():
            logger.error(f"InvoiceForm エラー: {form.errors}")

        if not formset.is_valid():
            logger.error(f"InvoiceItemFormSet エラー: {formset.errors}")

        if form.is_valid() and formset.is_valid():
            # 請求書を保存
            invoice = form.save(commit=False)
            invoice.creator = request.user
            invoice.save()

            # 各請求項目を保存
            for form_item in formset:
                item = form_item.save(commit=False)
                item.invoice = invoice  # 請求書に紐付け
                item.subtotal = item.quantity * item.unit_price  # 小計を計算
                item.save()

            # 確認画面にリダイレクト
            return redirect('invoice_confirm', pk=invoice.pk)
        else:
            # **フォームエラーをテンプレートに渡す**
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
def quotation_pdf(request, pk):
    quotation = Quotation.objects.get(pk=pk)
    items = QuotationItem.objects.filter(quotation=quotation)
    company = CompanyProfile.objects.first()  # 会社情報を取得

    total_amount = sum(item.subtotal for item in items)

    # **ロゴ・印鑑のフルパスを取得**
    logo_path = f'file://{os.path.join(settings.MEDIA_ROOT, company.logo.name)}' if company and company.logo else ''
    seal_path = f'file://{os.path.join(settings.MEDIA_ROOT, company.seal.name)}' if company and company.seal else ''

    # **HTMLテンプレートをレンダリング**
    html_string = render_to_string('docspdf/quotation_pdf.html', {
        'quotation': quotation,
        'items': items,
        'total_amount': total_amount,
        'company': company,
        'logo_path': logo_path,
        'seal_path': seal_path,
    })

    # **CSSのフルパスを取得**
    css_path = os.path.join(settings.STATICFILES_DIRS[0], 'css/style.css')

    # **WeasyPrintでPDFを生成**
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    css = CSS(filename=css_path)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="quotation_{quotation.quotation_number}.pdf"'
    html.write_pdf(response, stylesheets=[css])

    return response



@login_required
def create_quotation(request):
    QuotationItemFormSet = modelformset_factory(QuotationItem, form=QuotationItemForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = QuotationForm(request.POST)
        formset = QuotationItemFormSet(request.POST, queryset=QuotationItem.objects.none())
        if form.is_valid() and formset.is_valid():
            # 見積書を保存
            quotation = form.save(commit=False)
            quotation.creator = request.user
            quotation.save()

            # 各見積項目を保存
            for form_item in formset:
                item = form_item.save(commit=False)
                item.quotation = quotation  # 見積書に紐付け
                item.subtotal = item.quantity * item.unit_price  # 小計を計算
                item.save()

            # 確認画面にリダイレクト
            return redirect('quotation_confirm', pk=quotation.pk)
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
    quotation = Quotation.objects.get(pk=pk)
    items = QuotationItem.objects.filter(quotation=quotation)

    # 小計（全項目の合計）
    total_amount = sum(item.subtotal for item in items)

    # 消費税（10%）
    tax_amount = int(total_amount * 0.1)

    # 合計（小計 + 消費税）
    total_with_tax = total_amount + tax_amount

    # 会社情報を取得（データがなければ None）
    company = CompanyProfile.objects.first()

    return render(request, 'docspdf/quotation_confirm.html', {
        'quotation': quotation,
        'items': items,
        'total_amount': total_amount,
        'tax_amount': tax_amount,
        'total_with_tax': total_with_tax,
        'company': company,  # ← 修正: `company` を取得
        'user': request.user,  # ユーザー情報をテンプレートに渡す
    })


@login_required
def edit_quotation(request, pk):
    quotation = Quotation.objects.get(pk=pk)
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
def invoice_list(request):
    invoices = Invoice.objects.all().order_by('-created_at')
    return render(request, 'docspdf/invoice_list.html', {'invoices': invoices})


@login_required
def invoice_confirm(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    items = InvoiceItem.objects.filter(invoice=invoice)

    total_amount = sum(item.subtotal for item in items)

    return render(request, 'docspdf/invoice_confirm.html', {
        'invoice': invoice,
        'items': items,
        'total_amount': total_amount,
    })

@login_required
def invoice_pdf(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    items = InvoiceItem.objects.filter(invoice=invoice)
    company = CompanyProfile.objects.first()  # 会社情報を取得

    total_amount = sum(item.subtotal for item in items)

    # **ロゴ・印鑑のフルパスを取得**
    logo_path = f'file://{os.path.join(settings.MEDIA_ROOT, company.logo.name)}' if company and company.logo else ''
    seal_path = f'file://{os.path.join(settings.MEDIA_ROOT, company.seal.name)}' if company and company.seal else ''

    # **HTMLテンプレートをレンダリング**
    html_string = render_to_string('docspdf/invoice_pdf.html', {
        'invoice': invoice,
        'items': items,
        'total_amount': total_amount,
        'company': company,
        'logo_path': logo_path,
        'seal_path': seal_path,
    })

    # **CSSのフルパスを取得**
    css_path = os.path.join(settings.STATICFILES_DIRS[0], 'css/style.css')

    # **WeasyPrintでPDFを生成**
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    css = CSS(filename=css_path)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'
    html.write_pdf(response, stylesheets=[css])

    return response



@login_required
def edit_invoice(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    InvoiceItemFormSet = modelformset_factory(InvoiceItem, form=InvoiceItemForm, extra=0, can_delete=True)

    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        formset = InvoiceItemFormSet(request.POST, queryset=InvoiceItem.objects.filter(invoice=invoice))
        if form.is_valid() and formset.is_valid():
            # 請求書を保存
            invoice = form.save()

            # 各請求項目を保存
            items = formset.save(commit=False)
            for item in items:
                item.invoice = invoice  # 請求書に紐付け
                item.subtotal = item.quantity * item.unit_price  # 小計を計算
                item.save()

            # 削除された項目を削除
            for item in formset.deleted_objects:
                item.delete()

            # 確認画面にリダイレクト
            return redirect('invoice_confirm', pk=invoice.pk)
        else:
            # デバッグ用
            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)
    else:
        form = InvoiceForm(instance=invoice)
        formset = InvoiceItemFormSet(queryset=InvoiceItem.objects.filter(invoice=invoice))

    return render(request, 'docspdf/edit_invoice.html', {
        'form': form,
        'formset': formset,
    })
