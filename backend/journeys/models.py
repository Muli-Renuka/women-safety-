from django.conf import settings
from django.db import models
class Journey(models.Model):
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='journeys'); destination=models.CharField(max_length=200,blank=True); started_at=models.DateTimeField(auto_now_add=True); estimated_arrival=models.DateTimeField(null=True,blank=True); ended_at=models.DateTimeField(null=True,blank=True); check_in_interval_minutes=models.PositiveIntegerField(default=30); sharing_enabled=models.BooleanField(default=False); last_check_in=models.DateTimeField(null=True,blank=True); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-started_at']
