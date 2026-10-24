from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
@ensure_csrf_cookie
def health(request): return JsonResponse({'status':'ok','service':'ShadowMode API','notifications':'not_configured'})
urlpatterns = [path('admin/', admin.site.urls), path('api/health/', health), path('api/v1/auth/', include('accounts.urls')), path('api/v1/contacts/', include('contacts.urls')), path('api/v1/alerts/', include('alerts.urls')), path('api/v1/journeys/', include('journeys.urls'))]
