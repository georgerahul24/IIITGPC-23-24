from django.urls import path, include
from .views import FirstCase

urlpatterns = [
    path('', FirstCase.as_view()),
]
