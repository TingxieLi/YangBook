from django.urls import path
from .views import RegisterView, LoginView, EmailVerifyCodeView, LogoutView, ResetPasswordFirstView, ResetPasswordSecondView, UserInfoView, ChangeAvatarView, UserBookshelfView, UserHistoryView, UserAttentionView

app_name = 'user'
urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('email_verify_code', EmailVerifyCodeView.as_view(), name='email_verify_code'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('reset_password1', ResetPasswordFirstView.as_view(), name='reset_password1'),
    path('reset_password2', ResetPasswordSecondView.as_view(), name='reset_password2'),
    path('info', UserInfoView.as_view(), name='info'),
    path('collect', UserBookshelfView.as_view(), name='collect'),
    path('history', UserHistoryView.as_view(), name='history'),
    path('attention', UserAttentionView.as_view(), name='attention'),
    path('change_avatar', ChangeAvatarView.as_view(), name='change_avatar'),
]
