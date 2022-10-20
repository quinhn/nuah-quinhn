from django.shortcuts import render, redirect
from decouple import config
from . import api_teleport
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import logging

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

logger = logging.getLogger('main')


def home(request):
    return render(request, "authentication/index.html")

def pwd_policy(request):
    return render(request, "authentication/pwd_policy.html")

@csrf_exempt
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        if User.objects.filter(username=username):
            pass
        else:            
            myuser = User.objects.create_user(username,'',config('DJANGO_PASSWORD'))
            myuser.is_active = True
            myuser.save()
        password = request.POST['password']

        login_status = api_teleport.sign_in(
            config('API_URL'), 
            username, 
            password
        )
        user = authenticate(username=username, password=config('DJANGO_PASSWORD'))

        if (login_status == True) and (user is not None):
            login(request, user)
            messages.success(request, "Login successfully.")
            logger.info(f"User '{username}' login success.")
            return render(request, "authentication/change_pwd.html",{"fname":username})
        else:
            messages.error(request, "Login Fail. Please try again")
            logger.error(f"User '{username}' login fail.")
    return render(request, "authentication/index.html")

@csrf_exempt
def change_pwd(request):
    if request.method == "POST":
        username = request.POST['username']
        current_pwd = request.POST['current_pass']
        new_pwd_1 = request.POST['new_pass_1']
        new_pwd_2 = request.POST['new_pass_2']
        if new_pwd_1 == new_pwd_2:
            change_status = api_teleport.change_password(
                config('API_URL'),
                username,
                current_pwd,
                new_pwd_1
            )
            if change_status == True:
                messages.info(request, "Change password successfullly.")
                logger.info(f"User '{username}' change password success.")
                return redirect('home')
            else:
                messages.error(request, f"{change_status}.")
                logger.error(f"{change_status}")
        else:
            messages.error(request, "Change password fail.")
            logger.error(f"User '{username}' change new password not match.")
    # return redirect('home')
    return render(request, "authentication/change_pwd.html",{"fname":username})



@csrf_exempt
def forgot_pwd(request):
    if request.method == 'POST':
        username = request.POST['username']
        if User.objects.filter(username=username):
            pass
        else:            
            myuser = User.objects.create_user(username,'',config('DJANGO_PASSWORD'))
            myuser.is_active = True
            myuser.save()
        email = request.POST['email']

        reset_status = api_teleport.reset_password(
            config('API_URL'), 
            username, 
            email
        )

        user = authenticate(username=username, password=config('DJANGO_PASSWORD'))

        if (reset_status == True) and (user is not None) :
            login(request, user)
            messages.success(request, "Please check current password on your email.")
            logger.info(f"User '{username}' request reset password success.")
            return render(request, "authentication/change_pwd.html",{"fname":username})
        else: 
            messages.error(request, "Please try again.")
            logger.error(f"User '{username}' request reset password fail.")
    return render(request, "authentication/forgot_pwd.html")

@csrf_exempt
def verify_code(request):
    if request.method == 'POST':
        code = request.POST['code']
        username = request.POST['username']
        email = request.POST['email']
        
        code_status = api_teleport.verify_code(
            config('API_URL'),
            username,
            email,
            code
        )
        if code_status == True:
            user = authenticate(username=username, password=config('DJANGO_PASSWORD'))
            login(request, user)
            messages.info(request, "Reset password successfullly.")
            logger.info(f"User '{username}' reset password success.") 
            return render(request, "authentication/change_pwd.html",{"fname":username})
        else:
            messages.error(request, "Invalid code, Please try again.")
            logger.info(f"User '{username}' reset password fail.") 
    return redirect('forgot_pwd')
