from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    # TokenAuthentication
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    # 회원가입
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path("accounts/", include("accounts.urls")),
    path("deposits/", include("deposits.urls")),
    path("exchange/", include("exchange.urls")),
    path("databuilder/", include("databuilder.urls")),
    path("cards/", include("cards.urls")),
    path("api/v1/", include("articles.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# 프로젝트에서 사용할 주요 기능
# 1. 로그인 : dj-rest-auth/^login/$[name='rest_loin']
# 2. 로그아웃 : dj-rest-auth/^logout/$[name='rest_logout']
# 3. 유저정보반환 : dj-rest-auth/^user/$[name='rest_user_details']
# 4. 회원가입 : dj-rest-auth/registration/
#           : http://127.0.0.1:8000/dj-rest-auth/registration/ 접속 시 회원가입 입력 받을 필드 출력

# dj-rest-auth/ 경로는 기본 제공 엔드포인트
# 따로 입력하지 않아도 사용자 확인가능
# 로그인: dj-rest-auth/login/
# 로그아웃: dj-rest-auth/logout/
# 토큰 확인: dj-rest-auth/token/verify/
# 사용자 정보: dj-rest-auth/user/

# 주의 postman에서 사용자 정보에서 확인할때
# 'Token key' 이렇게 입력해야함! 앞에 'Token'입력하고 스페이스로 한칸 뛰고 부여받은 키값입력!
