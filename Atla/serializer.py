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


class PriorityScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriorityScore
        fields = '__all__'



class ObjectSerializer(serializers.ModelSerializer):
    priority_score = serializers.SerializerMethodField()
    priority_level = serializers.SerializerMethodField()

    class Meta:
        model = Object
        fields = [
            "id",
            "name",
            "region",
            "resource_type",
            "water_type",
            "fauna",
            "passport_date",
            "technical_condition",
            "latitude",
            "longitude",
            "pdf",
            "priority",  # если хочешь оставить старое поле
            "created_at",
            "priority_score",
            "priority_level",
        ]

    def get_priority_score(self, obj) -> int | None:
        if hasattr(obj, "priority_score"):
            return obj.priority_score.score
        return None

    def get_priority_level(self, obj) -> str | None:
        if hasattr(obj, "priority_score"):
            return obj.priority_score.level
        return None
