from django.urls import path, re_path, include
from .views import ProfileAPIView, RequestAuthSMSCodeAPIView, ConfirmAuthSMSCodeAPIView, WhoAmIView

urlpatterns = [
    path('api/v1/', include(
        [
            path(r'profiles/<str:invite_code>', ProfileAPIView.as_view()),
            path(r'auth/code_request', RequestAuthSMSCodeAPIView.as_view()),
            path(r'auth/confirm', ConfirmAuthSMSCodeAPIView.as_view()),
            path(r'whoami', WhoAmIView.as_view())
        ]
    ))
]
