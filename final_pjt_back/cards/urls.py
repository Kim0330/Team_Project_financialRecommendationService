from django.urls import path
from . import views

urlpatterns = [
    path('', views.card ),
    path('<int:pk>/', views.card_detail)
]