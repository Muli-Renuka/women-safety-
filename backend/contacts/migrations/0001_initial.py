from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(name='TrustedContact', fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('name',models.CharField(max_length=100)),('phone',models.CharField(max_length=25)),('email',models.EmailField(blank=True,max_length=254)),('relationship',models.CharField(blank=True,max_length=60)),('notify_on_sos',models.BooleanField(default=True)),('acknowledgement_preferred',models.BooleanField(default=False)),('ordering',models.PositiveIntegerField(default=0)),('created_at',models.DateTimeField(auto_now_add=True)),('updated_at',models.DateTimeField(auto_now=True)),('owner',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='trusted_contacts',to=settings.AUTH_USER_MODEL))], options={'ordering':['ordering','name']})]
