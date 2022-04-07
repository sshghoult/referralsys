from django.urls import path, re_path
from .views import ProfileAPIView

urlpatterns = [
    path(r'profile/<str:invite_code>', ProfileAPIView.as_view()),
]
