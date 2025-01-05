from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from allauth.account.adapter import get_adapter, DefaultAccountAdapter
from django.contrib.auth import get_user_model
from .models import User
UserModel = get_user_model()


# dj-rest-auth에서 회원가입 시 사용하는 기본 RegisterSerializer의 구조
# 기본 registerSerializer은 username, email, password 1, 2필드를 가지고 있음
# 회원가입을 처리하기 위해 데이터 유효성 검사, 사용자 생성, 비밀번호 저장 등을 담당
# RegisterSerializer를 custom model 과 연결시켜주기 위해서는 새로운 registerSerializer을 만들어야함
# 패키지 내부 설정값을 사용자 설정으로 변경


# dj_rest_auth.registration.serializers.RegisterSerializer 를 상속받아 필요한 부분을 추가
# 유저 기본 정보 + nickname 필드를 추가
class CustomRegisterSerializer(RegisterSerializer):
    # 필요한 필드들을 추가합니다.
    username = serializers.CharField(
                required=False,
                allow_blank=True,
                max_length=255
                )
    # 해당 필드도 저장 시 함께 사용하도록 설정합니다.
    nickname = serializers.CharField(max_length=100)
    email = serializers.EmailField(required=False)
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICES)
    occupation = serializers.ChoiceField(choices=User.OCCUPATION_CHOICES)


    # validated_data : 유효성 검사를 통과한 데이터가 저장된 객체
    # 사용자 객체를 생성하거나 저장할 때 사용 
    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            # nickname 필드 추가
            'nickname': self.validated_data.get('nickname', ''),
            'email': self.validated_data.get('email', ''),
            'gender': self.validated_data.get('gender', ''),
            'occupation': self.validated_data.get('occupation', '')
        } 
        # age, profile 사진은 기본값이 있기 때문에 필수가 아니라면 추가할 필요없음!

    # 아래 save가 없으면 회원가입 요청시 사용자 계정을 실제로 생성하고 데이터베이스에 저장하지 못함!
    def save(self, request):
        adapter = get_adapter()
        # 1. 사용자 객체 생성
        user = adapter.new_user(request)
        # 2. 검증된 데이터 사용
        self.cleaned_data = self.get_cleaned_data()
        # 3. 사용자 데이터 저장
        adapter.save_user(request, user, self)
        # 4. 커스터마이징 포인트
        self.custom_signup(request, user)
        # 5. 생성된 사용자 반환
        return user


# 마이페이지 또는 사용자 프로필 상세 정보용
# 여기서도 dj-rest-auth/dj_rest_auth/serializers.py 이걸 상속받을 것임!
# 로그인 시 유저정보 반환용
class CustomUserDetailsSerializer(UserDetailsSerializer):
   class Meta:
       model = User
       fields = ('username', 'nickname', 'email', 'age', 'profile_img', 'gender', 'occupation', 'data_joined')
       read_only_fields = ('username', 'data_joined')

# 마이페이지 조회용
class UserProfileSerializer(serializers.ModelSerializer):
   class Meta:
       model = User
       fields = ('id', 'username', 'nickname', 'email', 'age', 'profile_img', 'gender', 'occupation', 'data_joined')
       read_only_fields = ('id', 'username', 'data_joined')
       
# 마이페이지 수정용
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('nickname', 'email', 'age', 'gender', 'occupation')