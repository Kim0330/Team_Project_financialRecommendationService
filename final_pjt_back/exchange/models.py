from django.db import models

# Create your models here.
class Exchange(models.Model):
    cur_unit = models.CharField(max_length=100)             # 통화 코드 : "AED"
    cur_nm = models.CharField(max_length=100)               # 국가/통화명 : : "아랍에미리트 디르함"
    ttb = models.CharField(max_length=50)                   # 받으실 때(송금) : "288.78"
    tts = models.CharField(max_length=50)                   # 보내실때(송금) : "294.61"
    deal_bas_r = models.CharField(max_length=50)            # 매매 기준율 : "291.7"
    bkpr = models.CharField(max_length=50)                  # 장부가격 : "291"
    yy_efee_r = models.CharField(max_length=50)             # 년환가료율 : "0"
    ten_dd_efee_r = models.CharField(max_length=50)         # 10일환가료율 : "0"  # 추가 수수료
    kftc_deal_bas_r = models.CharField(max_length=50)       # 서울외국환중개 매매기준율 : "291"
    kftc_bkpr = models.CharField(max_length=50)             # 서울외국환중개 장부가격 : "291.7"

