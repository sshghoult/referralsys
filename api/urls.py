from django.urls import path, re_path
from .views import UserAPIView

urlpatterns = [
    path(r'profile/<str:invite_code>', UserAPIView.as_view()),
]
