import requests
from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Card
from . serializers import Cardserializer ,CardBenefitserializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
# Create your views here.

@api_view(['GET', 'POST'])
def card(request):
    if request.method == 'GET':
        cards = get_list_or_404(Card)
        serializer = Cardserializer(cards, many=True)
        return JsonResponse(serializer.data)

    elif request.method == "POST":
        serializer = Cardserializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['PUT', 'DELETE', 'GET'])
def card_detail(request, pk):
    card = Card.objects.get(pk=pk)
    if request.method == "PUT":
        serializer = CardBenefitserializer(data=request.data, instance=card)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        card.delete()
        return JsonResponse({'detail': '삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'GET':
        serializer = Cardserializer(card)
        return Response(serializer.data)