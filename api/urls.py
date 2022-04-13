from django.urls import path, re_path, include
from .views import ProfileAPIView, RequestAuthSMSCodeAPIView, ConfirmAuthSMSCodeAPIView

urlpatterns = [
    path('api/', include(
        [
            path(r'profiles/<str:invite_code>', ProfileAPIView.as_view()),
            path(r'auth/code_request', RequestAuthSMSCodeAPIView.as_view()),
            path(r'auth/confirm', ConfirmAuthSMSCodeAPIView.as_view()),
        ]
    ))
]
