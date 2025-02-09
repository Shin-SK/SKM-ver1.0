# customers/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('add/', views.add_or_edit_customer, name='add_customer'),
    path('edit/<int:customer_id>/', views.add_or_edit_customer, name='edit_customer'),
    path('delete/<int:customer_id>/', views.delete_customer, name='delete_customer'),
    path('export/', views.export_customers_csv, name='export_customers_csv'),
    path('import/', views.import_customers_csv, name='import_customers_csv'),  # インポートURLを追加
    path('import/confirm/', views.confirm_import, name='confirm_import'),
]
