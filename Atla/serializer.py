from rest_framework import serializers
from .models import ResourceType, WaterType, Object, PriorityScore, Region


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class ResourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceType
        fields = '__all__'


class WaterTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterType
        fields = '__all__'


class PriorityScoreSerializer(serializers.ModelSerializer):
    object_id = serializers.PrimaryKeyRelatedField(
        source="obj",
        read_only=True
    )

    class Meta:
        model = PriorityScore
        fields = ['id', 'object_id', 'obj', 'score', 'level', 'formula_version', 'updated_at']



class ObjectSerializer(serializers.ModelSerializer):
    pdf = serializers.FileField(
        required=False,
        allow_null=True,
        use_url=False,
        style={"type": "file"},
    )
    # Явно указываем формат для схемы Swagger/OpenAPI
    pdf.swagger_schema_fields = {"type": "string", "format": "binary"}
    pdf_url = serializers.SerializerMethodField(read_only=True)
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
            "pdf_url",
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

    def get_pdf_url(self, obj) -> str | None:
        """
        Возвращает абсолютный URL файла, если он загружен.
        """
        request = self.context.get("request")
        if obj.pdf:
            url = obj.pdf.url
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None
