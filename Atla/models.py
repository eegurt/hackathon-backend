from django.db import models

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
    region = models.CharField(max_length=100)
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE)
    water_type = models.ForeignKey(WaterType, on_delete=models.CASCADE)
    fauna = models.BooleanField(default=True)
    passport_date = models.DateField()
    technical_condition = models.IntegerField(default=0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    pdf = models.FileField(upload_to='passports/')
    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class PriorityScore(models.Model):
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    def __str__(self):
        return self.object.name
        