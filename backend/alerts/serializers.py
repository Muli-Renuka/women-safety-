from rest_framework import serializers
from .models import EmergencyAlert
class AlertSerializer(serializers.ModelSerializer):
    class Meta: model=EmergencyAlert; fields=['id','event_uuid','event_type','created_at','latitude','longitude','accuracy','location_timestamp','status','notification_status','cancelled','accidental','acknowledged_at']; read_only_fields=['id','status','cancelled','acknowledged_at']
    def validate(self,data):
        lat=data.get('latitude'); lon=data.get('longitude'); acc=data.get('accuracy')
        if (lat is None) != (lon is None): raise serializers.ValidationError('Latitude and longitude must be provided together.')
        if lat is not None and not -90 <= lat <= 90: raise serializers.ValidationError({'latitude':'Latitude must be between -90 and 90.'})
        if lon is not None and not -180 <= lon <= 180: raise serializers.ValidationError({'longitude':'Longitude must be between -180 and 180.'})
        if acc is not None and acc < 0: raise serializers.ValidationError({'accuracy':'Accuracy cannot be negative.'})
        return data
