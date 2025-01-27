"""
Django settings for final_pjt_back project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# evn 파일 경로지정을 위한 생성
import os
import environ

# 환경변수를 불러올 수 있는 상태로 설정
env=environ.Env(DEBUG=(bool, True))

# 환경변수를 읽어올 파일을 설정합니다.
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)

# 환경변수를 읽어옵니다.
FINANCE_API_KEY = env('FINANCE_API_KEY', default='default_value_if_not_set')
EXCHANGE_API_KEY = env('EXCHANGE_API_KEY', default='default_value_if_not_set' )


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_jhaj_gp3l97_jrgz#!%3h08xt_sw-k^em9ob(nl+y&iu2q=w5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # app 종류
    'accounts',
    'exchange',
    'deposits',
    'databuilder',
    'cards',
    'articles',
    'django_filters',
    # rest_framework 패키지
    'rest_framework',
    'django.contrib.sites',
    # 토근을 담아서 username 과 password 으로 Token을 발급받고 매 API 요청에 담아서 인증처리
    'rest_framework.authtoken',
    # 서버(백엔드)에서 요청을 보낼 때 프론트앤드 localhost로 보내지기 때문에 패키지 설치
    'corsheaders',
    # allauth 패키지 : 장고 프레임워크로 구성된 웹 어플리케이션에서 유저 가입,로그인,인증 등을 도와주는 패키지
    'allauth',
    'dj_rest_auth',
    'allauth.account',
    'allauth.socialaccount',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# social login시 필요! 
SITE_ID = 1

REST_FRAMEWORK = {
    # authentication token
    'DEFAULT_AUTHENTICATION_CLASSES' : [
        'rest_framework.authentication.TokenAuthentication',
    ],
    
    # permission
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

# Rest-AUTH 설정은 dj-rest-auth가 기본적으로 사용하는 시리얼라이저들을 우리가 커스텀한 시리얼라이저로 대체하기 위한 것
# rest-auth 가 회원 가입 시 구현한 serializer 를 호출하도록 설정합
REST_AUTH = {
    # 회원가입 재정의
    'REGISTER_SERIALIZER': 'accounts.serializers.CustomRegisterSerializer',
    # 사용자정보 확인
    'USER_DETAILS_SERIALIZER': 'accounts.serializers.CustomUserDetailsSerializer',
}

# 이메일 인증없이 회원가입
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'
#account 어댑터 설정
ACCOUNT_ADAPTER = 'accounts.models.CustomAccountAdapter'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:5174',
    'http://localhost:5175'    
]

ROOT_URLCONF = 'final_pjt_back.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'final_pjt_back.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

# 정적 파일 추가 경로 지정
STATICFILES_DIRS = [
    BASE_DIR /'static',
]

# 사용자 이미지 업로드 위함 
MEDIA_ROOT = BASE_DIR/'media'
MEDIA_ROOT = '/media/'
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# django의 AbstractUser 사용(user model customizing)
# [app].[모델명]
AUTH_USER_MODEL = 'accounts.User'
