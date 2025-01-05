from django.test import TestCase
import requests
# Create your tests here.
api_key='4PkL0rlVpfhnc91X0PwPtDyFlbKnrLC7'
URL='https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=4PkL0rlVpfhnc91X0PwPtDyFlbKnrLC7&searchdate=20180102&data=AP01'

datas = requests.get(URL).json()
for data in datas:
    print(data['cur_unit'])
    print(data['ttb'])
    print(data['tts'])
    print(data['deal_bas_r'])



# "result": 1,
# "cur_unit": "AED",
# "ttb": "288.78",
# "tts": "294.61",
# "deal_bas_r": "291.7",
# "bkpr": "291",
# "yy_efee_r": "0",
# "ten_dd_efee_r": "0",
# "kftc_bkpr": "291",
# "kftc_deal_bas_r": "291.7",
# "cur_nm": "아랍에미리트 디르함"