import requests
from django.shortcuts import get_object_or_404, get_list_or_404
from django.conf import settings
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Deposit, DepositOption, Saving, SavingOption
from .serializers import DepositSerializer, DepositOptionSerializer, SavingSerializer, SavingOptionSerializer
from django.http import JsonResponse

from rest_framework import generics
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .filters import DepositOptionFilter, SavingOptionFilter, DepositFilter, SavingFilter
# Create your views here.


# 과정
# 1. OPEN API 받아오기
    # env 파일은 pull 하지 않으면 매번 생성해야 함!
# 2. 데이터 생성 후 저장 
    # 데이터 추출 후 저장(생성)하기
    # 예금 데이터와 옵션은 외래키로 연결되어있기에 따로 url을 따로 줘서 생성하면 오류 발생
    # 데이터의 무결성과 일관성을 유지하려면 데이터는 되도록 한 번에 적기


# 캐시데이터를 사용해야햐나?????? 아니면 매번 변경사항이 있는지 검사해야하나???
@api_view(['GET'])
def make_fin_data(request): 
    # API를 통해 데이터를 처음 모델 객체를 가져오는 경우는 데이터를 검증하고 직렬화하는 것이 필수!
    
    Api_key = settings.FINANCE_API_KEY
    DEPOSIT_API_URL = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={Api_key}&topFinGrpNo=020000&pageNo=1'
    SAVING_API_URL = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={Api_key}&topFinGrpNo=020000&pageNo=1'


    # 예금 데이터
    response = requests.get(DEPOSIT_API_URL)
    response.encoding = 'utf-8'
    data = response.json()
    print(data)
    base_datas = data.get('result').get('baseList')
    option_datas = data.get('result').get('optionList')
    
    for base_data in base_datas:
        
        # 데이터가 없으면 생성
        serializer = DepositSerializer(data={        # 키워드는 data 매개변수로 전달해야함!(serializer 구조)
        'fin_co_no':base_data.get('join_deny', '-1'), # -1 은 기본값 데이터가 존재하지 않거나 값이 NONE인 경우 반환
        'kor_co_nm':base_data.get('kor_co_nm', '-1'),
        'fin_prdt_cd':base_data.get('fin_prdt_cd', '-1'),
        'fin_prdt_nm':base_data.get('fin_prdt_nm', '-1'),
        'join_way':base_data.get('join_way', '-1'),
        'mtrt_int':base_data.get('mtrt_int', '-1'),
        'spcl_cnd':base_data.get('spcl_cnd', '-1'),
        'join_member':base_data.get('join_member', '-1'),
        'join_deny':base_data.get('join_deny', -1),
        'max_limit':base_data.get('max_limit', -1),
        'etc_note':base_data.get('etc_note', '-1')
        })
        
        if Deposit.objects.filter(fin_prdt_cd=base_data.get('fin_prdt_cd')).exists():
            continue
        else:
            if serializer.is_valid(raise_exception=True):
                deposit_data = serializer.save()
                # print(deposit_data)
                # print(deposit_data.fin_prdt_nm)
                

    # 예금 옵션 데이터 추출 후 저장(생성)하기
    for option_data in option_datas:
        fin_prdt_cd = option_data.get('fin_prdt_cd')
        deposit = Deposit.objects.filter(fin_prdt_cd=fin_prdt_cd).first()
        # print(deposit)
        # print(deposit.id)
        
        if deposit:
            intr_rate = option_data.get('intr_rate')
            intr_rate2 = option_data.get('intr_rate2')
            if intr_rate is None:
                intr_rate = -1
            if intr_rate2 is None:
                intr_rate2 = -1
            option_serializer = DepositOptionSerializer(data={ 
            'deposit':deposit.id,
            'fin_prdt_cd' :option_data.get('fin_prdt_cd', '-1'),
            'intr_rate_type_nm':option_data.get('intr_rate_type_nm', '-1'),
            'save_trm':option_data.get('save_trm', -1),
            # 값이 생성되지 않은 이유 : 오류 none 값이 있었음
            'intr_rate':intr_rate,
            'intr_rate2':intr_rate2
            })
            if DepositOption.objects.filter(
                deposit=deposit, fin_prdt_cd=fin_prdt_cd,
                intr_rate_type_nm=option_data.get('intr_rate_type_nm'),save_trm=option_data.get('save_trm'), 
                intr_rate=intr_rate, intr_rate2=intr_rate2 ).exists():
                continue
            else:
                if option_serializer.is_valid():
                    deposit_option_data=option_serializer.save(deposit=deposit)
                    # print(deposit_option_data)
                    # print(deposit_option_data.fin_prdt_cd)
                # 에러 메세지 꼭 확인하기
                else:
                    print(option_serializer.errors)


    # 적금 데이터 가져오기
    response = requests.get(SAVING_API_URL)
    response.encoding = 'utf-8'
    data = response.json()
    saving_base_datas = data.get('result').get('baseList')
    saving_option_datas = data.get('result').get('optionList')

    for saving_data in saving_base_datas:
        make_saving_data = {
        'fin_co_no':saving_data.get('join_deny', '-1'), 
        'kor_co_nm':saving_data.get('kor_co_nm', '-1'),
        'fin_prdt_cd':saving_data.get('fin_prdt_cd', '-1'),
        'fin_prdt_nm':saving_data.get('fin_prdt_nm', '-1'),
        'join_way':saving_data.get('join_way', '-1'),
        'mtrt_int':saving_data.get('mtrt_int', '-1'),
        'spcl_cnd':saving_data.get('spcl_cnd', '-1'),
        'join_member':saving_data.get('join_member', '-1'),
        'join_deny':saving_data.get('join_deny', -1),
        'max_limit':saving_data.get('max_limit', -1),
        'etc_note':saving_data.get('etc_note', '-1')
        }

        if Saving.objects.filter(fin_prdt_cd=saving_data.get('fin_prdt_cd')).exists():
            continue
        else:
            serializer = SavingSerializer(data=make_saving_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

    for saving_option in saving_option_datas:
        fin_prdt_cd = saving_option.get('fin_prdt_cd')
        saving = Saving.objects.filter(fin_prdt_cd=fin_prdt_cd).first()
        
        intr_rate=saving_option.get('intr_rate')
        if intr_rate is None:
            intr_rate = -1
        intr_rate2=saving_option.get('intr_rate2')
        if intr_rate2 is None:
            intr_rate2 = -1
        making_saving_option_data = {
            'fin_prdt_cd' : saving_option.get('fin_prdt_cd'),
            'intr_rate_type_nm': saving_option.get('intr_rate_type_nm', '-1'),
            'rsrv_type_nm': saving_option.get('rsrv_type_nm', '-1'),
            'intr_rate': intr_rate,
            'intr_rate2': intr_rate2,
            'save_trm': saving_option.get('save_trm', -1),
        }

        if SavingOption.objects.filter(
            saving=saving, 
            fin_prdt_cd=fin_prdt_cd,
            intr_rate_type_nm=saving_option.get('intr_rate_type_nm'),
            rsrv_type_nm=saving_option.get('rsrv_type_nm'),
            intr_rate=intr_rate,
            intr_rate2=intr_rate2,
            save_trm=saving_option.get('save_trm')
        ).exists():continue
        else: 
            saving_option_serializer = SavingOptionSerializer(data=making_saving_option_data)
            if saving_option_serializer.is_valid(raise_exception=True):
                saving_option_serializer.save(saving=saving)
            else:
                print(saving_option_serializer.errors)
    return Response({'message': 'Data has been created!'})



# 예금 정보 조회
@api_view(['GET'])
def deposit_data(request):
    if request.method == 'GET':
        deposits = Deposit.objects.all()
        serializer = DepositSerializer(deposits, many=True)
        return Response(serializer.data)

# 예금 정보 상세 조회
@api_view(['GET'])
def deposit_detail(request, fin_prdt_cd):
    deposit = get_object_or_404(Deposit, fin_prdt_cd=fin_prdt_cd)
    if request.method == 'GET':
        serializer = DepositSerializer(deposit)
        return Response(serializer.data)


# 예금 옵션 전체 조회하기
@api_view(['GET'])
def deposit_option_data(request, fin_prdt_cd):
    depositoptions = DepositOption.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = DepositOptionSerializer(depositoptions, many=True)
    return Response(serializer.data)

# 예금 옵션 전체 조회하기
@api_view(['GET'])
def deposit_option(request):
    print(1)
    depositoptions = DepositOption.objects.all()
    serializer = DepositOptionSerializer(depositoptions, many=True)
    return Response(serializer.data)



# 예금 옵션 상세 조회하기
@api_view(['GET'])
def deposit_option_detail(request, fin_prdt_cd, pk):
    deposit=get_object_or_404(Deposit, fin_prdt_cd=fin_prdt_cd)
    deposit_option = get_object_or_404(DepositOption, pk=pk, deposit=deposit)
    if request.method == "GET":
        serializer = DepositOptionSerializer(deposit_option)
        return Response(serializer.data)


# 적금 정보 조회하기
@api_view(['GET'])
def saving_data(request):
    if request.method == 'GET':
        savings = Saving.objects.all()
        serializer = SavingSerializer(savings, many=True)
        return Response(serializer.data)
    
# 적금 정보 상세 조회
@api_view(['GET'])
def saving_detail(request, fin_prdt_cd):
    saving = get_object_or_404(Saving, fin_prdt_cd=fin_prdt_cd)
    if request.method == 'GET':
        serializer = SavingSerializer(saving)
        return Response(serializer.data)

# 적금 옵션 전체 조회하기
@api_view(['GET'])
def saving_option_data(request, fin_prdt_cd):
    savingoptions = SavingOption.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = SavingOptionSerializer(savingoptions, many=True)
    return Response(serializer.data)    

# 적금 옵션 상세 조회하기
@api_view(['GET'])
def saving_option_detail(request, fin_prdt_cd, pk):
    saving=get_object_or_404(Saving, fin_prdt_cd=fin_prdt_cd)
    saving_option = get_object_or_404(SavingOption, pk=pk, saving=saving)
    if request.method == "GET":
        serializer = SavingOptionSerializer(saving_option)
        return Response(serializer.data)


# 예적금 필터링
# 예금 상품의 개월 수

# @api_view(['GET'])
# def deposit_1_months(request):
#     print(1)
#     deposits = DepositOption.objects.filter(save_trm=1)
#     serializer = DepositOptionSerializer(deposits, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# def deposit_3_months(request):
#     deposits = DepositOption.objects.filter(save_trm=3)
#     serializer = DepositOptionSerializer(deposits, many=True)
#     return Response(serializer.data)
# @api_view(['GET'])
# def deposit_6_months(request):
#     deposits = DepositOption.objects.filter(save_trm=6)
#     serializer = DepositOptionSerializer(deposits, many=True)
#     return Response(serializer.data)
# @api_view(['GET'])
# def deposit_12_months(request):
#     deposits = DepositOption.objects.filter(save_trm=12)
#     serializer = DepositOptionSerializer(deposits, many=True)
#     return Response(serializer.data)
# @api_view(['GET'])
# def deposit_24_months(request):
#     deposits = DepositOption.objects.filter(save_trm=24)
#     serializer = DepositOptionSerializer(deposits, many=True)
#     return Response(serializer.data)
# @api_view(['GET'])
# def deposit_36_months(request):
#     deposits = DepositOption.objects.filter(save_trm=36)
#     serializer = DepositOptionSerializer(deposits, many=True)
#     return Response(serializer.data)

# # 적금 상품의 개월 수
# @api_view(['GET'])
# def saving_1_months(request):
#     savings = SavingOption.objects.filter(save_trm=1)
#     serializer = SavingOptionSerializer(savings, many=True)
#     return Response(serializer.data)
# @api_view(['GET'])
# def saving_3_months(request):
#     savings = SavingOption.objects.filter(save_trm=3)
#     serializer = SavingOptionSerializer(savings, many=True)
#     return Response(serializer.data)
# @api_view(['GET'])
# def saving_6_months(request):
#     savings = SavingOption.objects.filter(save_trm=6)
#     serializer = SavingOptionSerializer(savings, many=True)
#     return Response(serializer.data)
# @api_view(['GET'])
# def saving_12_months(request):
#     savings = SavingOption.objects.filter(save_trm=12)
#     serializer = SavingOptionSerializer(savings, many=True)
#     return Response(serializer.data)
# @api_view(['GET'])
# def saving_24_months(request):
#     savings = SavingOption.objects.filter(save_trm=24)
#     serializer = SavingOptionSerializer(savings, many=True)
#     return Response(serializer.data)
# @api_view(['GET'])
# def saving_36_months(request):
#     savings = SavingOption.objects.filter(save_trm=36)
#     serializer = SavingOptionSerializer(savings, many=True)
#     return Response(serializer.data)


# # 예금 단리/복리
# @api_view(['GET'])
# def deposit_simple_interest(request):
#     deposits = DepositOption.objects.filter(intr_rate_type_nm='단리')
#     serializer = DepositOptionSerializer(deposits, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def deposit_compound_interest(request):
#     deposits = DepositOption.objects.filter(intr_rate_type_nm='복리')
#     serializer = DepositOptionSerializer(deposits, many=True)
#     return Response(serializer.data)


# # 적금 단리/복리
# @api_view(['GET'])
# def saving_simple_interest(request):
#     savings = SavingOption.objects.filter(intr_rate_type_nm='단리')
#     serializer = SavingOptionSerializer(savings, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def saving_compound_interest(request):
#     savings = SavingOption.objects.filter(intr_rate_type_nm='복리')
#     serializer = SavingOptionSerializer(savings, many=True)
#     return Response(serializer.data)

# # 은행별
# @api_view(['GET'])
# def bank_filter(request, kor_co_nm):
#     deposits = Deposit.objects.filter(kor_co_nm=kor_co_nm)
#     savings = Saving.objects.filter(kor_co_nm=kor_co_nm)
#     return Response({
#         "deposits": DepositSerializer(deposits, many=True).data,
#         "savings": SavingSerializer(savings, many=True).data
#     })



class DepositOptionListView(generics.ListAPIView):
    queryset = DepositOption.objects.all()
    serializer_class = DepositOptionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DepositOptionFilter   # 필터링할 필드

class SavingOptionListView(generics.ListAPIView):
    queryset = SavingOption.objects.all()
    serializer_class = SavingOptionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SavingOptionFilter   # 필터링할 필드

class DepositListView(generics.ListAPIView):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DepositFilter   # 필터링할 필드

class SavingListView(generics.ListAPIView):
    queryset = Saving.objects.all()
    serializer_class = SavingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SavingFilter   # 필터링할 필드

