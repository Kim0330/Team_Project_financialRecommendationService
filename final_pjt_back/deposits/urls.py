from django.urls import path
from . import  views
from . views import DepositOptionListView, SavingOptionListView, DepositListView, SavingListView


urlpatterns = [
    
    # 예금/예금옵션데이터 생성
    path('make_fin_data/', views.make_fin_data),

    # 예금
    path('deposit_data/', views.deposit_data),
    path('deposit_option_data/<str:fin_prdt_cd>/', views.deposit_option_data),
    path('deposit_option_data/', views.deposit_option),
    path('deposit_data/<str:fin_prdt_cd>/', views.deposit_detail),
    path('deposit_option_data/<str:fin_prdt_cd>/<int:pk>/', views.deposit_option_detail),
    
    # 적금 
    path('saving_data/', views.saving_data),
    path('saving_option_data/<str:fin_prdt_cd>/', views.saving_option_data),
    path('saving_data/<str:fin_prdt_cd>/', views.saving_detail),
    path('saving_option_data/<str:fin_prdt_cd>/<int:pk>/', views.saving_option_detail),
    
    # 예적금 필터링

    # 계속해서 빈 [] 이 생성, 데이터가 제대로 들어옴에도 불구하고 데이터가 생성이 되지 않음
    # 예금 상품의 개월 수
    # path('deposit_option_data/1_months/', views.deposit_1_months),
    # path('deposit_option_data/3_months/', views.deposit_3_months),
    # path('deposit_option_data/6_months/', views.deposit_6_months),
    # path('deposit_option_data/12_months/', views.deposit_12_months),
    # path('deposit_option_data/24_months/', views.deposit_24_months),
    # path('deposit_option_data/36_months/', views.deposit_36_months),

    # # 적금 상품의 개월 수
    # path('saving_option_data/1_months/', views.saving_1_months),
    # path('saving_option_data/3_months/', views.saving_3_months),
    # path('saving_option_data/6_months/', views.saving_6_months),
    # path('saving_option_data/12_months/', views.saving_12_months),
    # path('saving_option_data/24_months/', views.saving_24_months),
    # path('saving_option_data/36_months/', views.saving_36_months),

    # # 예금 단리/ 복리
    # path('deposit_option_data/simple_interest/', views.deposit_simple_interest),
    # path('deposit_option_data/compound_interest/', views.deposit_compound_interest),

    # # 적금 단리/ 복리
    # path('saving_option_data/simple_interest/', views.saving_simple_interest),
    # path('saving_option_data/compound_interest/', views.saving_compound_interest),
    
    # # 은행별분류 
    # # 우리은행 한국스탠다드차타드은행 아이엠뱅크 부산은행 광주은행 제주은행 경남은행 중소기업은행 한국산업은행
    # # 국민은행 신한은행 농협은행주식회사 하나은행 주식회사 케이뱅크 수협은행 토스뱅크 주식회사
    # path('bank_filter/<str:bank_name>/', views.bank_filter),
    

    path('deposit-options/', DepositOptionListView.as_view(), name='deposit-options'),
    path('saving-options/', SavingOptionListView.as_view(), name='saving-options'),
    path('deposit-filter/', DepositListView.as_view(), name='deposit-filter'),
    path('saving-filter/', SavingListView.as_view(), name='saving-filter'),


    # Url
    # http://127.0.0.1:8000/deposits/deposit-options/?save_trm=1
    # http://127.0.0.1:8000/deposits/deposit-options/?intr_rate_type_nm=단리
    # http://127.0.0.1:8000/deposits/deposit-filter/?kor_co_nm=우리은행
    # http://127.0.0.1:8000/deposits/saving-filter/?kor_co_nm=국민은행

    

]