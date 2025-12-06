from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
from .services.priority import calculate_priority_score


class Region(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class ResourceType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class WaterType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
# Create your models here.
class Object(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE)
    water_type = models.ForeignKey(WaterType, on_delete=models.CASCADE)
    fauna = models.BooleanField(default=True)
    passport_date = models.DateField()
    technical_condition = models.IntegerField(default=0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    pdf = models.FileField(upload_to='passports/')
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class PriorityLevel(models.TextChoices):
    LOW = "low", _("Низкий")
    MEDIUM = "medium", _("Средний")
    HIGH = "high", _("Высокий")


class PriorityScore(models.Model):
    obj = models.OneToOneField(
        Object,
        on_delete=models.CASCADE,
        related_name="priority_score"
    )

    # Числовой приоритет
    score = models.IntegerField(default=0)

    # Уровень риска (низкий/средний/высокий)
    level = models.CharField(
        max_length=10,
        choices=PriorityLevel.choices,
        default=PriorityLevel.LOW,
    )

    # Версия формулы приоритезации (можно менять в будущем)
    formula_version = models.CharField(
        max_length=20,
        default="v1"
    )

    # Дата автоматического обновления
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.obj.name} — {self.score} ({self.level})"

    # Основной метод пересчёта
    def recalc(self, today: date | None = None, save: bool = True):
        """
        Пересчитать score и level на основе объекта.
        """
        score = calculate_priority_score(self.obj, today=today)
        self.score = score
        self.level = self._detect_level(score)

        if save:
            self.save()

        return self.score, self.level

    @staticmethod
    def _detect_level(score: int) -> str:
        """
        Классификация по ТЗ:
        • ≥ 12 → Высокий
        • 6–11 → Средний
        • < 6 → Низкий
        """
        if score >= 12:
            return PriorityLevel.HIGH
        if score >= 6:
            return PriorityLevel.MEDIUM
        return PriorityLevel.LOW