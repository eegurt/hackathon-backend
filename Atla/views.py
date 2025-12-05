from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ResourceType, WaterType, Object, PriorityScore
from .serializer import ResourceTypeSerializer, WaterTypeSerializer, ObjectSerializer, PriorityScoreSerializer


class ResourceTypeViewSet(viewsets.ModelViewSet):
    queryset = ResourceType.objects.all()
    serializer_class = ResourceTypeSerializer


class WaterTypeViewSet(viewsets.ModelViewSet):
    queryset = WaterType.objects.all()
    serializer_class = WaterTypeSerializer


class ObjectViewSet(viewsets.ModelViewSet):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer


class PriorityScoreViewSet(viewsets.ModelViewSet):
    queryset = PriorityScore.objects.all()
    serializer_class = PriorityScoreSerializer
