from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import TrustedContact
from .serializers import ContactSerializer
class ContactViewSet(viewsets.ModelViewSet):
    serializer_class=ContactSerializer; permission_classes=[IsAuthenticated]
    def get_queryset(self): return TrustedContact.objects.filter(owner=self.request.user)
    def perform_create(self,serializer): serializer.save(owner=self.request.user)
