from django.conf import settings
from django.db import models
class TrustedContact(models.Model):
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='trusted_contacts')
    name=models.CharField(max_length=100); phone=models.CharField(max_length=25); email=models.EmailField(blank=True); relationship=models.CharField(max_length=60,blank=True)
    notify_on_sos=models.BooleanField(default=True); acknowledgement_preferred=models.BooleanField(default=False); ordering=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['ordering','name']
    def __str__(self): return self.name
