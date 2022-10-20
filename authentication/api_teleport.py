from decouple import config
import requests
import json


def get_headers(api_url: str):
    data = {"username": config('API_USERNAME'), "password": config('API_PASSWORD')}
    r = requests.post(
        api_url + "/token/",
        data=data,
        verify= False,
    )
    if r.status_code == 200:
        access_token = json.loads(r.text)["access_token"]
        headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "Authorization": "Bearer {}".format(access_token),
        }
        return headers
    return False


def sign_in(api_url: str, username: str ,password: str):
    headers = get_headers(api_url)
    data= {"username":username,"password":password}
    r = requests.post(
        config('API_URL') + "/user/validate_passwd/",
        headers=headers,
        data=json.dumps(data),
        verify= False,
    )
    if r.status_code == 200:
        access_token = json.loads(r.text)["status"]
        return access_token
    return False


def reset_password(api_url: str,username:str, email: str):
    headers = get_headers(api_url)
    data= {"username":username,"email":email}
    r = requests.post(
        config('API_URL') + "/check-email/",
        headers=headers,
        data=json.dumps(data),
        verify= False,
    )
    if r.status_code == 200:
        access_token = json.loads(r.text)['status']
        return access_token
    return False

def verify_code(api_url: str,username:str, email: str, code:str):
    headers = get_headers(api_url)
    data= {"username":username,"email":email,"code":code }
    r = requests.post(
        config('API_URL') + "/passwd/forgot/",
        headers=headers,
        data=json.dumps(data),
        verify= False,
    )
    if r.status_code == 200:
        access_token = json.loads(r.text)['status']
        return access_token
    return False

def change_password(api_url: str, username: str, currentpasswd: str, newpasswd: str):
    headers = get_headers(api_url)
    data= {"username":username,"currentpasswd":currentpasswd,"newpasswd":newpasswd}
    r = requests.put(
        config('API_URL') + "/passwd/user-change/",
        headers=headers,
        data=json.dumps(data),
        verify= False,
    )
    status = json.loads(r.text)
    if r.status_code == 200 and status['status'] == True:
        return True
    return status['error']