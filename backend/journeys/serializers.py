from rest_framework import serializers
from .models import Journey
class JourneySerializer(serializers.ModelSerializer):
    class Meta: model=Journey; fields=['id','destination','started_at','estimated_arrival','ended_at','check_in_interval_minutes','sharing_enabled','last_check_in']; read_only_fields=['id','started_at','ended_at','last_check_in']
