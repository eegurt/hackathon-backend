from rest_framework import serializers
from .models import ResourceType, WaterType, Object, PriorityScore


class ResourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceType
        fields = '__all__'


class WaterTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterType
        fields = '__all__'


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = '__all__'


class PriorityScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriorityScore
        fields = '__all__'
