from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import BicycleViewSet, ReservationViewSet

router= DefaultRouter()
router.register(r"bicycle", BicycleViewSet, basename="bicycle")
router.register(r"reservation", ReservationViewSet, basename="reservation")

urlpatterns = [
    path("", include(router.urls)),
]



