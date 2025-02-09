import logging
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import InventoryItem
from datetime import datetime

logger = logging.getLogger('django')

# 保存前（編集時）のログ
@receiver(pre_save, sender=InventoryItem)
def log_inventory_pre_save(sender, instance, **kwargs):
    # 保存前のインスタンスを取得
    if instance.pk:  # 既存データの場合のみ（新規作成は対象外）
        try:
            old_instance = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            return
        # 変更内容を比較してログを記録
        instance._changes = []
        for field in ['product_name', 'stock_count', 'product_code', 'notes']:
            old_value = getattr(old_instance, field, None)
            new_value = getattr(instance, field, None)
            if old_value != new_value:
                instance._changes.append(f"{field} from '{old_value}' to '{new_value}'")

# 保存後のログ
@receiver(post_save, sender=InventoryItem)
def log_inventory_post_save(sender, instance, created, **kwargs):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user = getattr(instance, '_current_user', 'Unknown')  # 操作者情報
    if created:
        # 新規作成のログ
        logger.info(
            f"[{current_time}] User: {user} created InventoryItem ID={instance.pk} - "
            f"Name: {instance.product_name}, Stock: {instance.stock_count}, Product Code: {instance.product_code}"
        )
    else:
        # 編集のログ（変更内容を記録）
        changes = getattr(instance, '_changes', [])
        if changes:
            logger.info(
                f"[{current_time}] User: {user} updated InventoryItem ID={instance.pk} - Changes: {', '.join(changes)}"
            )

# 削除時のログ
@receiver(post_delete, sender=InventoryItem)
def log_inventory_delete(sender, instance, **kwargs):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user = getattr(instance, '_current_user', 'Unknown')  # 操作者情報
    logger.info(
        f"[{current_time}] User: {user} deleted InventoryItem ID={instance.pk} - "
        f"Name: {instance.product_name}, Stock: {instance.stock_count}, Product Code: {instance.product_code}"
    )
