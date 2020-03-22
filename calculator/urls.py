from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('frequency/', views.frequency, name='frequency'),
    path('result/', views.result, name='result'),
]
