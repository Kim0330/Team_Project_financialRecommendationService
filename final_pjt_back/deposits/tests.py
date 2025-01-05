from django.conf import settings
# open API 가져오기
import requests
# deposit(예금)
Api_key = '88c4635eddb49d9cd76da88c25ffab2d'
API_URL = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={Api_key}&topFinGrpNo=020000&pageNo=1'

data = requests.get(API_URL).json()

base_datas = data.get('result').get('baseList')
# print (base_datas['fin_prdt_cd'])

option_datas = data.get('result').get('optionList')
# print(option_datas)


# for data in option_datas:
#     name = data.get('save_trm')
#     print(name)/
#         for datas in option_datas:
#             if datas.get('fin_prdt_cd') == 'WR0001B':
#                 print(datas)

# for data in base_datas:
#     name = data.get('fin_prdt_cd')
#     print(name)

# 우리은행 한국스탠다드차타드은행 아이엠뱅크 부산은행 광주은행 제주은행 경남은행 중소기업은행 한국산업은행
# 국민은행 신한은행 농협은행주식회사 하나은행 주식회사 케이뱅크 수협은행 토스뱅크 주식회사
'''
# 정기예금
fin_co_no = 금융회사 코드
kor_co_nm = 금융회사 명
fin_prdt_cd = 금융상품 코드
fin_prdt_nm = 금융 상품명
join_way = 가입 방법
mtrt_int = 만기 후 이자율
spcl_cnd = 우대 조건
join_member = 가입대상
join_deny = 가입제한
max_limit = 최고한도
---
# 정기예금 옵션목록 => 금융상품에 대해 선택 가능한 추가적인 조건들/ 상품의 특성을 설명
fin_co_no = 금융회사 코드
fin_prdt_cd = 금융상품 코드
intr_rate_type = 저축 금리 유형
intr_rate_type_nm = 저축 금리 유형명
save_trm = 저축기간[단위:개월]
intr_rate = 저축 금리[소수점 2자리]
intr_rate2 = 최고 우대 금리[소수점 2자리]
'''



SAVING_API_URL = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={Api_key}&topFinGrpNo=020000&pageNo=1'


data = requests.get(SAVING_API_URL).json()
datas = data.get('result').get('baseList')
print(datas)