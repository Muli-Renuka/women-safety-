from django.urls import path
from .views import AlertListCreate, AlertDetail, AcknowledgeView, CancelView
urlpatterns=[path('',AlertListCreate.as_view()),path('<int:pk>/',AlertDetail.as_view()),path('<int:pk>/acknowledge/',AcknowledgeView.as_view()),path('<int:pk>/cancel/',CancelView.as_view())]
