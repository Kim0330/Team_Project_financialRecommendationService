from django.db import models
from django.conf import settings
# Create your models here.

# 예금
class Deposit(models.Model):
    # recomm_user = models.ManyToManyField(settings.AUTH_USER_MODEL)  # 사용자 데이터 분석을 통한 맞춤 추천을 위해서는 다대다 연결 필요
    fin_co_no = models.TextField()                                  # 금융회사 코드 : '0017801'
    kor_co_nm = models.CharField(max_length=100)                    # 금융회사 명    : '토스뱅크 주식회사'
    fin_prdt_cd = models.CharField(max_length=100)                  # 금융상품 코드 : '1001202000002'
    fin_prdt_nm = models.TextField()                                # 금융 상품명 : '토스뱅크 먼저 이자 받는 정기예금'
    join_way = models.CharField(max_length=100)                     # 가입 방법      : '스마트폰'
    mtrt_int = models.TextField()                                   # 만기 후 이자율 : '· 만기 후 1개월 이내 : 만기시점 기본금리 X 50% \n· 만기 후 1개월 초과 3개월 이내 : 만기시점 기본금리 X 20% \n· 만기 후 3개월 초과 : 연 0.10%'
    spcl_cnd = models.TextField()                                   # 우대 조건 : '우대조건 없음'
    join_member = models.TextField()                                # 가입대상 : '토스뱅크 통장 또는 토스뱅크 서브 통장을 보유한 만 17세 이상 실명의 개인'
    join_deny = models.IntegerField()                               # 가입제한    : '1'  Ex) 1:제한없음, 2:서민전용, 3:일부제한
    # 여기 단계일까? 
    max_limit = models.IntegerField(null=True)                      # 최고한도 : 1000000000
    etc_note = models.TextField()

# 정기예금 옵션목록 => 금융상품에 대해 선택 가능한 추가적인 조건들/ 상품의 특성을 설명    
class DepositOption(models.Model):
    deposit = models.ForeignKey(Deposit,on_delete=models.CASCADE)       # 위 deposit과 연결된 외래키
    fin_prdt_cd = models.TextField()                                    # 금융상품코드     
    intr_rate_type_nm = models.TextField()                              # 저축 금리 유형명 : '단리'
    save_trm = models.IntegerField()                                    # 저축기간[단위:개월] : '6'
    # decimalField 를 저장하고 views에서 초기값을 -1로 저장해서 에러가 뜸!
    intr_rate = models.FloatField()                                     # 저축 금리[소수점 2자리] : 3
    intr_rate2 = models.FloatField()                                    # 최고 우대 금리[소수점 2자리] : 3




# 적금 
class Saving(models.Model):
    fin_co_no = models.TextField()                                  # 금융회사 코드 : '0010001'
    kor_co_nm = models.CharField(max_length=100)                    # 금융회사 명    : '우리은행'
    fin_prdt_cd = models.CharField(max_length=100)                  # 금융상품 코드 : 'WR0001F'
    fin_prdt_nm = models.TextField()                                # 금융 상품명 : '우리SUPER주거래적금'
    join_way = models.CharField(max_length=100)                     # 가입 방법      : '영업점,인터넷,스마트폰,전화(텔레뱅킹)'
    mtrt_int = models.TextField()                                   # 만기 후 이자율 : '· 만기 후\n- 1개월이내 : 만기시점약정이율×50%\n- 1개월초과 6개월이내: 만기시점약정이율×30%\n- 6개월초과 : 만기시점약정이율×20%\n\n※ 만기시점 약정이율 : 일반정기적금 금리'
    spcl_cnd = models.TextField()                                   # 우대 조건 : '우대조건 없음'
    join_member = models.TextField()                                # 가입대상 : '실명의 개인'
    join_deny = models.IntegerField()                               # 가입제한    : '1'  Ex) 1:제한없음, 2:서민전용, 3:일부제한
    # 여기 단계일까? 
    max_limit = models.IntegerField(null=True)                      # 최고한도 : null
    etc_note = models.TextField()
    
    
    
class SavingOption(models.Model):
    saving = models.ForeignKey(Saving, on_delete=models.CASCADE)
    fin_prdt_cd = models.CharField(max_length=100)                      # 금융상품 코드 : '220002101'       
    intr_rate_type_nm = models.TextField()                              # 저축 금리 유형명 : '단리'
    rsrv_type_nm = models.TextField()                                   # 적립 유형명 : '자유적립식'
    save_trm = models.IntegerField()                                    # 저축기간[단위:개월] : '6'
    intr_rate = models.FloatField()                                     # 저축 금리[소수점 2자리] : 3.25
    intr_rate2 = models.FloatField()                                    # 최고 우대 금리[소수점 2자리] : 5.35
    