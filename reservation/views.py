from django.shortcuts import render
from rest_framework import viewsets , permissions
from rest_framework.viewsets import ModelViewSet
from .models import Bicycle,Reservation
from .serializers import BicycleSerializer, ReservationSerializer

class BicycleViewSet(viewsets.ModelViewSet):
    queryset= Bicycle.objects.all()
    serializer_class = BicycleSerializer
    permission_classes = [permissions.IsAuthenticated]


class IsOwnerOrAdmin (permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user
          

class ReservationViewSet (viewsets.ModelViewSet):
    queryset = Reservation.objects.all ()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user= self.request.user
        if user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(user=user)
    
    def get_permissions(self):
        if self.action in ["create","retrieve","partial_update"]:
            return [permissions.IsAuthenticated()]
        elif self.action in ["update","list","destroy"]:
            return [permissions.IsAuthenticated(),IsOwnerOrAdmin()]
        else:
            return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
       