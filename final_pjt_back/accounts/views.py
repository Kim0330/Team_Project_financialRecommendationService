from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer, UserProfileUpdateSerializer
from .models import User

# Create your views here.


# 유저의 마이페이지 정보 확인 및 수정
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile_page(request, username):
    # 요청을 보낸 유저와 유저프로필 url 상의 유저가 같을때(동일인물)
    if request.user.username == username:
        
        if request.method == 'GET':
            # get_user_model() : settings.py 에 정의된 user 모델 가져와서 있으면 객체반환 없으면 404 에러
            user = get_object_or_404(get_user_model(),username=username)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            user = get_object_or_404(get_user_model(),username=username)
            serializer = UserProfileUpdateSerializer(instance=user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def user_delete(request, username):
    if request.method == 'DELETE':
        if request.user.username == username:
            user = User.objects.get(username=username)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

# def user_info(request):
#     pass 
