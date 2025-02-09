from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import InventoryItem
from .forms import InventoryItemForm

# 在庫リスト表示ビュー
@login_required
def inventory_list(request):
    """
    全社員が閲覧できる在庫リスト
    """
    items = InventoryItem.objects.all()
    return render(request, 'inventory/inventory_list.html', {'items': items})

# 在庫の追加・編集ビュー（管理者のみ）
@user_passes_test(lambda u: u.is_staff)
def edit_inventory(request, item_id=None):
    """
    在庫情報の追加・編集
    """
    item = get_object_or_404(InventoryItem, id=item_id) if item_id else None
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            instance = form.save(commit=False)
            instance._current_user = request.user.username  # 操作者をセット
            instance.save()
            return redirect('inventory_list')
    else:
        form = InventoryItemForm(instance=item)
    return render(request, 'inventory/edit_inventory.html', {'form': form})

# 在庫の削除ビュー（管理者のみ）
@user_passes_test(lambda u: u.is_staff)
def delete_inventory(request, item_id):
    """
    在庫情報の削除
    """
    item = get_object_or_404(InventoryItem, id=item_id)
    item._current_user = request.user.username  # 操作者をセット
    item.delete()
    return redirect('inventory_list')


import csv
from django.http import HttpResponse

@user_passes_test(lambda u: u.is_staff)
def export_inventory_csv(request):
    """
    在庫データをCSV形式でエクスポート
    """
    # HTTPレスポンスの設定
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory.csv"'

    # CSVライターを作成
    writer = csv.writer(response)
    # ヘッダー行
    writer.writerow(['ID', '商品名', '在庫数', '商品コード', '備考', '画像URL'])

    # 在庫データを取得
    items = InventoryItem.objects.all()
    for item in items:
        writer.writerow([
            item.id,
            item.product_name,
            item.stock_count,
            item.product_code,
            item.notes or '',
            request.build_absolute_uri(item.image.url) if item.image else '画像なし'
        ])

    return response

import os
from django.conf import settings
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def inventory_logs(request):
    """
    在庫の変更履歴をテーブル形式で表示
    """
    log_file_path = os.path.join(settings.BASE_DIR, 'logs/changes.log')
    parsed_logs = []

    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as log_file:
            for line in log_file:
                # 重要なログだけを解析
                if "User:" in line:
                    # ログを解析して情報を抽出
                    try:
                        time_part, user_action = line.strip().split("] User: ")
                        time = time_part.replace("[", "").strip()
                        user, details = user_action.split(" ", 1)
                        parsed_logs.append({
                            'time': time,
                            'user': user,
                            'details': details,
                        })
                    except ValueError:
                        continue  # フォーマット外のログはスキップ

    return render(request, 'inventory/inventory_logs.html', {'logs': parsed_logs})


@login_required
def inventory_list(request):
    """
    全社員が閲覧できる在庫リスト（商品名・商品コードで検索可能）
    """
    query = request.GET.get('q', '')  # 商品名での検索
    product_code_query = request.GET.get('product_code', '')  # 商品コードでの検索
    items = InventoryItem.objects.all()

    if query:
        items = items.filter(product_name__icontains=query)  # 商品名で部分一致検索
    
    if product_code_query:
        items = items.filter(product_code__icontains=product_code_query)  # 商品コードで部分一致検索

    return render(request, 'inventory/inventory_list.html', {'items': items, 'query': query, 'product_code_query': product_code_query})


import csv
from io import TextIOWrapper
from django.contrib import messages
from .forms import InventoryCSVImportForm

@user_passes_test(lambda u: u.is_staff)
def import_inventory_csv(request):
    """
    在庫データのCSVインポート
    """
    if request.method == 'POST':
        form = InventoryCSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
            reader = csv.DictReader(csv_file)
            for row in reader:
                product_name = row.get('商品名')
                stock_count = row.get('在庫数')
                product_code = row.get('商品コード')
                notes = row.get('備考')

                # 空の在庫数があれば0に設定
                stock_count = int(stock_count) if stock_count else 0

                # すでに同じproduct_codeが存在するか確認
                if InventoryItem.objects.filter(product_code=product_code).exists():
                    # 既存の商品があればスキップまたは更新する処理
                    continue  # 重複するproduct_codeがあればスキップ
                    # もし更新する場合は以下のように変更できます
                    # item = InventoryItem.objects.get(product_code=product_code)
                    # item.stock_count = stock_count
                    # item.save()
                else:
                    # データベースに保存（追記モード）
                    InventoryItem.objects.create(
                        product_name=product_name,
                        stock_count=stock_count,
                        product_code=product_code,
                        notes=notes
                    )

            messages.success(request, "CSVデータをインポートしました！")
            return redirect('inventory_list')
    else:
        form = InventoryCSVImportForm()

    return render(request, 'inventory/import_inventory.html', {'form': form})
