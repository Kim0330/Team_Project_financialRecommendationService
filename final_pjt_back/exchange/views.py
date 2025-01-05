from django.conf import settings
from django.shortcuts import render
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Exchange
from .serializers import ExchangeSerializer
import requests
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime, timedelta


# Create your views here.

# 환율 정보는 자주 갱신되고 변동성이 크기 때문에 update_or_create 보다는 delete가 더 적합
@api_view(['GET'])
def exchange(request):
    print("0번")
    Api_key = settings.EXCHANGE_API_KEY
    
    # 오늘 날짜 환율
    today = datetime.now().strftime('%Y%m%d')
    print(today)
    EXCHANGE_API_URL = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={Api_key}&searchdate={today}&data=AP01'

    # SSL 인증서 에러 verify=False 추가, 그러나 권장하지 않음.
    response = requests.get(EXCHANGE_API_URL)
    response.encoding = 'utf-8'
    datas = response.json()
    
    
    # 오늘 데이터가 없으면 어제 데이터 시도
    if not datas:
        print("오늘 데이터 없음, 어제 데이터 시도")
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
        print(yesterday)
        EXCHANGE_API_URL = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={Api_key}&searchdate={yesterday}&data=AP01'
        
        response = requests.get(EXCHANGE_API_URL)
        response.encoding = 'utf-8'
        datas = response.json()
    
    #늘 이렇게 디버깅 하기!
    # print("1번")
    if Exchange.objects.all():
        # print("2번")
        Exchange.objects.all().delete()
    if datas: 
        # print("3번")
        for data in datas:
            # 데이터 중 옛통화가 있어서 제거하기
            if data.get('cur_unit')=='KRW' or data.get('ttb') != '0':
                exchange_data = { 
                    'cur_unit' : data.get('cur_unit','-1'),
                    'cur_nm' : data.get('cur_nm','-1'),
                    'ttb' : data.get('ttb','-1'),
                    'tts' : data.get('tts','-1'),
                    'deal_bas_r' : data.get('deal_bas_r','-1'),
                    'bkpr' : data.get('bkpr','-1'),
                    'yy_efee_r' : data.get('yy_efee_r','-1'),
                    'ten_dd_efee_r' : data.get('ten_dd_efee_r','-1'),
                    'kftc_deal_bas_r' : data.get('kftc_deal_bas_r','-1'),
                    'kftc_bkpr'  : data.get('kftc_bkpr','-1'),
                }
            else: 
                continue
            
            serializer = ExchangeSerializer(data=exchange_data)
            # 여기서는 단일 객체를 검사 후 저장
            
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        
        
        # 프론트로 보내기위해서는 단일 객체가 아닌 전체 객체 보내기
        exchanges = Exchange.objects.all()
        # print(exchanges)
        serializer = ExchangeSerializer(exchanges, many=True)
        
        # print(serializer.data)
        return Response(serializer.data)
    
    return Response({"error": "환율 데이터 실패"}, status=status.HTTP_404_NOT_FOUND)


# 확인용
api_view(['GET'])
def exchange_check(request):
    if request.method == "GET":
        exchange = Exchange.objects.all()
        serializer = ExchangeSerializer(exchange, many=True)
        return Response(serializer.data, safe=False)