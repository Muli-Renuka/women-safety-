from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import EmergencyAlert
from .serializers import AlertSerializer
class AlertListCreate(generics.ListCreateAPIView):
    serializer_class=AlertSerializer; permission_classes=[IsAuthenticated]
    def get_queryset(self): return EmergencyAlert.objects.filter(owner=self.request.user)
    def create(self,request,*args,**kwargs):
        s=self.get_serializer(data=request.data); s.is_valid(raise_exception=True); event=s.validated_data['event_uuid']
        existing=EmergencyAlert.objects.filter(owner=request.user,event_uuid=event).first()
        if existing: return Response(AlertSerializer(existing).data,status=200)
        obj=s.save(owner=request.user,status='SERVER_ACCEPTED',notification_status='NOT_CONFIGURED')
        return Response(AlertSerializer(obj).data,status=status.HTTP_201_CREATED)
class AlertDetail(generics.RetrieveAPIView):
    serializer_class=AlertSerializer; permission_classes=[IsAuthenticated]
    def get_queryset(self): return EmergencyAlert.objects.filter(owner=self.request.user)
class AcknowledgeView(APIView):
    def post(self,request,pk):
        try: alert=EmergencyAlert.objects.get(pk=pk,owner=request.user)
        except EmergencyAlert.DoesNotExist: return Response({'detail':'Not found.'},status=404)
        alert.status='ACKNOWLEDGED'; alert.acknowledged_at=timezone.now(); alert.save(update_fields=['status','acknowledged_at','updated_at']); return Response(AlertSerializer(alert).data)
class CancelView(APIView):
    def post(self,request,pk):
        try: alert=EmergencyAlert.objects.get(pk=pk,owner=request.user)
        except EmergencyAlert.DoesNotExist: return Response({'detail':'Not found.'},status=404)
        alert.cancelled=True; alert.status='CANCELLED'; alert.accidental=bool(request.data.get('accidental',False)); alert.save(update_fields=['cancelled','status','accidental','updated_at']); return Response(AlertSerializer(alert).data)
