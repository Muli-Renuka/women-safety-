from rest_framework.routers import DefaultRouter
from .views import JourneyViewSet
router=DefaultRouter(); router.register('',JourneyViewSet,basename='journey')
urlpatterns=router.urls
