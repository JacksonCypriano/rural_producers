from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import DashboardView, DashboardAPIView
from .viewsets import FarmerViewSet, FarmViewSet, HarvestViewSet, CropViewSet

router = DefaultRouter()
router.register(r'farmers', FarmerViewSet, basename='farmer')
router.register(r'farms', FarmViewSet, basename='farm')
router.register(r'harvests', HarvestViewSet, basename='harvest')
router.register(r'crops', CropViewSet, basename='crop')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('api/dashboard/', DashboardAPIView.as_view(), name='dashboard-api'),
]
