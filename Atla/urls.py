from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResourceTypeViewSet, WaterTypeViewSet, ObjectViewSet, PriorityScoreViewSet

router = DefaultRouter()
router.register(r'resource-types', ResourceTypeViewSet)
router.register(r'water-types', WaterTypeViewSet)
router.register(r'objects', ObjectViewSet)
router.register(r'priority-scores', PriorityScoreViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
