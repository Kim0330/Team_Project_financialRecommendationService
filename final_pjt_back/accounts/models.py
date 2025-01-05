from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter


# Create your models here.
# AbstractUser : django에서 많이 쓰는 user model customizing
# abstractUser 모델을 상속한 user 모델
# django user model 이 가지고 있는 핵심 field 
# : id / password / last_login / is_superuser / username / first_name / last_name / email / is_staff / is_active / date_joined


# 절대! Auth_USER_MODEL을 지정하기 전에 migrate 하지 않기!
class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    nickname = models.CharField(max_length=50)
    email = models.EmailField(unique=True, blank=True, null=True)
    age = models.IntegerField(default=0)
    profile_img = models.ImageField(upload_to='images/', default='C:/Users/SSAFY/Desktop/final_pjt/final-pjt/final_pjt_back/static/images/default_profile.png')
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    OCCUPATION_CHOICES = [
        ('S', '학생'),
        ('D', '개발자'),
    ]
    occupation = models.CharField(max_length=1, choices=OCCUPATION_CHOICES)
    data_joined = models.DateTimeField(auto_now_add=True)


    # 예적금 모델을 이미 만들어놔서 이건 패스! 뷰에서 받아오기 
    # deposit_period = models.IntegerField(blank=True, null=True)
    # saving_period = models.IntegerField(blank=True, null=True)


# 회원가입시 추가로 입력되지 않았던 정보들 저장하기
class CustomAccountAdapter(DefaultAccountAdapter):
   def save_user(self, request, user, form, commit=True):
        from allauth.account.utils import user_email, user_field, user_username
        
        data = form.cleaned_data
        if data.get("username"):
            user_field(user, "username", data.get("username"))
        if data.get("email"):
            user_field(user, "email", data.get("email"))
        if data.get("nickname"):
            user_field(user, "nickname", data.get("nickname"))
        if data.get("gender"):
            user_field(user, "gender", data.get("gender"))
        if data.get("occupation"):
            user_field(user, "occupation", data.get("occupation"))
        if data.get("age"):
            user_field(user, "age", data.get("age"))

        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        
        self.populate_username(request, user)
        
        if commit:
            user.save()
        return user
        