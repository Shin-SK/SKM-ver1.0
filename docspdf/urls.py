from django.urls import path
from . import views

urlpatterns = [
    path('create_quotation/', views.create_quotation, name='create_quotation'),
    path('list/', views.quotation_list, name='quotation_list'),
    path('pdf/<int:pk>/', views.quotation_pdf, name='quotation_pdf'),
    path('confirm/<int:pk>/', views.quotation_confirm, name='quotation_confirm'),
    path('edit/<int:pk>/', views.edit_quotation, name='edit_quotation'),  # 編集用ビュー
    path('create_invoice/', views.create_invoice, name='create_invoice'),
    path('invoice_list/', views.invoice_list, name='invoice_list'),  # 請求書一覧ページ
    path('invoice_confirm/<int:pk>/', views.invoice_confirm, name='invoice_confirm'),
    path('invoice_pdf/<int:pk>/', views.invoice_pdf, name='invoice_pdf'),
    path('edit_invoice/<int:pk>/', views.edit_invoice, name='edit_invoice'),
    path('invoice_preview/<int:pk>/', views.invoice_preview, name='invoice_preview'),
]
