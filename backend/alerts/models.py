import uuid
from django.conf import settings
from django.db import models
class EmergencyAlert(models.Model):
    STATUS=[('SERVER_ACCEPTED','Server accepted'),('ACKNOWLEDGED','Acknowledged'),('CANCELLED','Cancelled')]
    event_uuid=models.UUIDField(default=uuid.uuid4); owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='emergency_alerts')
    event_type=models.CharField(max_length=40,default='SOS'); created_at=models.DateTimeField(); latitude=models.FloatField(null=True,blank=True); longitude=models.FloatField(null=True,blank=True); accuracy=models.FloatField(null=True,blank=True); location_timestamp=models.DateTimeField(null=True,blank=True)
    status=models.CharField(max_length=30,choices=STATUS,default='SERVER_ACCEPTED'); notification_status=models.CharField(max_length=30,default='NOT_CONFIGURED'); cancelled=models.BooleanField(default=False); accidental=models.BooleanField(default=False); acknowledged_at=models.DateTimeField(null=True,blank=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['owner','event_uuid'],name='unique_alert_uuid_per_owner')]; ordering=['-created_at']
    def __str__(self): return f'{self.event_type} {self.event_uuid}'
class AlertRecipient(models.Model):
    alert=models.ForeignKey(EmergencyAlert,on_delete=models.CASCADE,related_name='recipients'); contact_name=models.CharField(max_length=100); destination_masked=models.CharField(max_length=100,blank=True); status=models.CharField(max_length=30,default='NOT_CONFIGURED'); submitted_at=models.DateTimeField(null=True,blank=True); acknowledged_at=models.DateTimeField(null=True,blank=True)
