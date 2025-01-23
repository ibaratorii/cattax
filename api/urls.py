from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VideoAnalysisViewSet

router = DefaultRouter()
router.register(r'analysis', VideoAnalysisViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 