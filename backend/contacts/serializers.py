from rest_framework import serializers
from .models import TrustedContact
class ContactSerializer(serializers.ModelSerializer):
    class Meta: model=TrustedContact; fields=['id','name','phone','email','relationship','notify_on_sos','acknowledgement_preferred','ordering','created_at','updated_at']; read_only_fields=['id','created_at','updated_at']
    def validate_phone(self,value):
        cleaned=''.join(c for c in value if c.isdigit() or c=='+')
        if len(''.join(c for c in cleaned if c.isdigit())) < 7: raise serializers.ValidationError('Enter a valid phone number.')
        return value
