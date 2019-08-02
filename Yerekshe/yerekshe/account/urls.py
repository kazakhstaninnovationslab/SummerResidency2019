from django.urls import path,include
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.home, name="home"),
    path('sign_up/', views.register, name="register"),
    path('login/', views.login, name='login'),
    path('test/', views.test, name = 'test'),
    path('predict/', views.report, name ='report'),
]
