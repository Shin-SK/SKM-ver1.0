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
    在庫データをCSV形式でエクスポート（image_url はファイル名だけ）
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory.csv"'

    writer = csv.writer(response)
    writer.writerow(["id", "product_name", "stock_count", "product_code", "notes", "image_filename", "updated_at"])

    for item in InventoryItem.objects.all():
        writer.writerow([
            item.id,
            item.product_name,
            item.stock_count,
            item.product_code,
            item.notes or '',
            item.image.name if item.image else '',  # 画像のファイル名だけ出力
            item.updated_at.strftime("%Y-%m-%d %H:%M:%S")
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
    在庫データのCSVインポート（image_filename のみ指定）
    """
    if request.method == 'POST':
        form = InventoryCSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
            reader = csv.DictReader(csv_file)

            for row in reader:
                product_name = row.get('product_name')
                stock_count = row.get('stock_count')
                product_code = row.get('product_code')
                notes = row.get('notes')
                image_filename = row.get('image_filename')  # 画像ファイル名だけ取得

                # 在庫数が空なら0に設定
                stock_count = int(stock_count) if stock_count else 0

                # 画像のパスをセット（存在しなければNone）
                image_path = f"inventory_images/{image_filename}" if image_filename else None
                if image_path and not os.path.exists(os.path.join(settings.MEDIA_ROOT, image_path)):
                    image_path = None  # ファイルが存在しない場合はNoneにする

                # 既存の商品があればスキップまたは更新する処理
                if InventoryItem.objects.filter(product_code=product_code).exists():
                    continue  # 重複するproduct_codeがあればスキップ
                else:
                    # データベースに保存（画像は存在する場合のみセット）
                    InventoryItem.objects.create(
                        product_name=product_name,
                        stock_count=stock_count,
                        product_code=product_code,
                        notes=notes,
                        image=image_path if image_path else None  # 画像がある場合のみセット
                    )

            messages.success(request, "CSVデータをインポートしました！（image_filename対応）")
            return redirect('inventory_list')
    else:
        form = InventoryCSVImportForm()

    return render(request, 'inventory/import_inventory.html', {'form': form})
