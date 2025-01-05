from django.urls import path
from . import views

urlpatterns = [
    # 유저 프로필(마이페이지)
    path('page/<str:username>/', views.user_profile_page),
    # 유저 정보
    # path('info/<str:username>/', views.user_info),
    # 유저 삭제
    path('delete/<str:username>/', views.user_delete),
]
