from django.urls import path
from . import views

urlpatterns = [
    path('', views.exchange),
    path('exchange_check/', views.exchange_check)
]