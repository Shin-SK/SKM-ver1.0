import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Employee

logger = logging.getLogger('django')

# 保存（作成・編集）時のログ
@receiver(post_save, sender=Employee)
def log_employee_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"User: Unknown created Employee ID={instance.pk} with data: {instance.__dict__}")
    else:
        changes = []
        for field in ['first_name', 'last_name', 'department', 'email', 'phone_number']:
            old_value = instance.__dict__.get(f"_original_{field}")
            new_value = getattr(instance, field, None)
            if old_value != new_value:
                changes.append(f"{field} from '{old_value}' to '{new_value}'")
        if changes:
            logger.info(f"User: Unknown updated Employee ID={instance.pk}: " + "; ".join(changes))


# 削除時のログ
@receiver(post_delete, sender=Employee)
def log_employee_delete(sender, instance, **kwargs):
    logger.info(f"User: Unknown deleted Employee ID={instance.pk} with data: {instance.__dict__}")
