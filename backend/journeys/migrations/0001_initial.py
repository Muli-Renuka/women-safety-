from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(name='Journey', fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('destination',models.CharField(blank=True,max_length=200)),('started_at',models.DateTimeField(auto_now_add=True)),('estimated_arrival',models.DateTimeField(blank=True,null=True)),('ended_at',models.DateTimeField(blank=True,null=True)),('check_in_interval_minutes',models.PositiveIntegerField(default=30)),('sharing_enabled',models.BooleanField(default=False)),('last_check_in',models.DateTimeField(blank=True,null=True)),('created_at',models.DateTimeField(auto_now_add=True)),('owner',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='journeys',to=settings.AUTH_USER_MODEL))], options={'ordering':['-started_at']})]
