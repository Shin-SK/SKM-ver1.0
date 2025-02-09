from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('edit/', views.edit_inventory, name='edit_inventory'),  # 新しい在庫を追加
    path('edit/<int:item_id>/', views.edit_inventory, name='edit_inventory'),
    path('delete/<int:item_id>/', views.delete_inventory, name='delete_inventory'),
    path('export-csv/', views.export_inventory_csv, name='export_inventory_csv'),
    path('logs/', views.inventory_logs, name='inventory_logs'),
    path('import/', views.import_inventory_csv, name='import_inventory_csv'),
]

