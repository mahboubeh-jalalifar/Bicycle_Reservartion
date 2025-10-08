from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
User = get_user_model ()

class IsOwnerOrAdmin (permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return getattr (obj,"user",None) == request.user
        

class UserViewSet (viewsets.ModelViewSet):
    queryset = User.objects.all ()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ["create"]:
            return [permissions.AllowAny()]
        elif self.action in ["destroy"]:
            return [permissions.IsAdminUser()]
        else:
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]