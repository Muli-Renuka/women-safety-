from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from contacts.models import TrustedContact
from alerts.models import EmergencyAlert
from django.utils import timezone
import uuid
class ApiTests(TestCase):
 def setUp(self):
  self.user=get_user_model().objects.create_user(username='renuka-test',password='StrongPass!234'); self.other=get_user_model().objects.create_user(username='other-test',password='StrongPass!234'); self.client=APIClient(); self.client.force_authenticate(self.user)
 def test_contact_is_private(self):
  c=TrustedContact.objects.create(owner=self.other,name='Private',phone='+911234567890'); r=self.client.get('/api/v1/contacts/'); self.assertEqual(r.status_code,200); self.assertEqual(r.data,[])
 def test_alert_create_and_idempotency(self):
  event=str(uuid.uuid4()); payload={'event_uuid':event,'event_type':'SOS','created_at':timezone.now().isoformat()}
  a=self.client.post('/api/v1/alerts/',payload,format='json'); b=self.client.post('/api/v1/alerts/',payload,format='json'); self.assertIn(a.status_code,[200,201]); self.assertEqual(b.status_code,200); self.assertEqual(EmergencyAlert.objects.filter(owner=self.user,event_uuid=event).count(),1)
 def test_invalid_coordinates(self):
  r=self.client.post('/api/v1/alerts/',{'event_uuid':str(uuid.uuid4()),'event_type':'SOS','created_at':timezone.now().isoformat(),'latitude':120,'longitude':2},format='json'); self.assertEqual(r.status_code,400)
 def test_unauthenticated_contacts(self):
  self.client.force_authenticate(None); self.assertEqual(self.client.get('/api/v1/contacts/').status_code,403)
