from django.contrib import admin
from django.urls import path, include
from pybo.views import base_views
from django.contrib.auth import views as auth_views
from common.views import account_views, profile_views


urlpatterns = [
    # 기본 URL인 /localhosts:8000/페이지 요청은 'pybo/account_views.py'의 index함수를 실행시킨다.
    path('admin/', admin.site.urls),
    # pybo/로 시작되는 페이지 요청은 pybo/urls.py파일에 있는 url매핑을 참고하여 처리 하여라
    path('pybo/', include('pybo.urls')),
    # http://localhost:8000/common/으로 시작하는 URL은 모두 common/urls.py 파일을 참조할 것이다.
    path('common/', include('common.urls')),
    # 기본 URL인 /localhosts:8000/페이지 요청은 'pybo/views/base_views'의 index함수를 실행시킨다.
    path('', base_views.index, name='index'),  # '/' 에 해당되는 path

    # 비밀번호 초기화
    path('password_reset/', account_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_change/', account_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_reset/done/', account_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', account_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # 추가
    # path('password_change/done/', views.PasswordChangeView.as_view(), name='password_change_done'),
    path('password_change/', account_views.PasswordChangeView.as_view(), name='password_change'),
    # http://127.0.0.1:8000/password_reset/

    path('accounts/',include('allauth.urls')),

]