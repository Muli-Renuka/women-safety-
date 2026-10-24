from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Journey
from .serializers import JourneySerializer
class JourneyViewSet(viewsets.ModelViewSet):
    serializer_class=JourneySerializer; permission_classes=[IsAuthenticated]
    def get_queryset(self): return Journey.objects.filter(owner=self.request.user)
    def perform_create(self,serializer): serializer.save(owner=self.request.user)
    @action(detail=True,methods=['post'])
    def check_in(self,request,pk=None):
        obj=self.get_object(); obj.last_check_in=timezone.now(); obj.save(update_fields=['last_check_in']); return Response(self.get_serializer(obj).data)
    @action(detail=True,methods=['post'])
    def end(self,request,pk=None):
        obj=self.get_object(); obj.ended_at=timezone.now(); obj.save(update_fields=['ended_at']); return Response(self.get_serializer(obj).data)
