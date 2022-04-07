from django.urls import path, re_path
from .views import ProfileAPIView, RequestAuthSMSCodeAPIView, ConfirmAuthSMSCodeAPIView

urlpatterns = [
    path(r'profiles/<str:invite_code>', ProfileAPIView.as_view()),
    path(r'auth/code_request', RequestAuthSMSCodeAPIView.as_view()),
    path('auth/confirm', ConfirmAuthSMSCodeAPIView.as_view()),

]
