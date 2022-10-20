from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path("",views.home, name=""),
    path('home', views.home,name = "home"),
    path('pwd_policy', views.pwd_policy,name = "pwd_policy"),
    path('signin', views.signin, name= "signin"),
    path('forgot_pwd', views.forgot_pwd, name= "forgot_pwd"),
    path('change_pwd', views.change_pwd, name= "change_pwd"),
    path('verify_code', views.verify_code, name= "verify_code"),
]