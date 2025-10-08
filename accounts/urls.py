from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

router = DefaultRouter()
router.register(r"user",UserViewSet,basename="user")

urlpatterns = [
    path("",include(router.urls)),
    path("token/obtain/",TokenObtainPairView.as_view(),name="token-obtain-pair"),
    path("token/refresh/",TokenRefreshView.as_view(),name="token-refresh"),
]

