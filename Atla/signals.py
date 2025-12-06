from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Object, PriorityScore
from .services.priority import calculate_priority_score
from .models import PriorityLevel
from datetime import date


@receiver(post_save, sender=Object)
def update_priority_score(sender, instance: Object, created, **kwargs):
    score = calculate_priority_score(instance, today=date.today())

    if score >= 12:
        level = PriorityLevel.HIGH
    elif score >= 6:
        level = PriorityLevel.MEDIUM
    else:
        level = PriorityLevel.LOW

    priority_obj, _ = PriorityScore.objects.get_or_create(obj=instance)
    priority_obj.score = score
    priority_obj.level = level
    priority_obj.save()

    # Обновляем priority у Object без вызова сигналов
    Object.objects.filter(id=instance.id).update(priority=score)