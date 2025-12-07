from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegionViewSet, ResourceTypeViewSet, WaterTypeViewSet, ObjectViewSet, PriorityScoreViewSet

router = DefaultRouter()
router.register(r'regions', RegionViewSet)
router.register(r'resource-types', ResourceTypeViewSet)
router.register(r'water-types', WaterTypeViewSet)
router.register(r'objects', ObjectViewSet)
router.register(r'priority-scores', PriorityScoreViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
