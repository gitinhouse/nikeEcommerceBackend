from django.conf import settings
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from urllib.parse import urlencode
from typing import Dict, Any
import requests
import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth import login 
from django.http import HttpRequest


User = get_user_model() 

GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'
LOGIN_URL = f'{settings.BASE_APP_URL}/internal/login'

# Exchange authorization token with access token
def google_get_access_token(code: str, redirect_uri: str) -> str:
    data = {
        'code': code,
        'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
        'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)
    if not response.ok:
        raise ValidationError('Could not get access token from Google.')
    
    access_token = response.json()['access_token']

    return access_token

# Get user info from google
def google_get_user_info(access_token: str) -> Dict[str, Any]:
    response = requests.get(
        GOOGLE_USER_INFO_URL,
        params={'access_token': access_token}
    )

    if not response.ok:
        raise ValidationError('Could not get user info from Google.')
    
    return response.json()


def get_user_data(validated_data , request: HttpRequest):
    domain = settings.BASE_API_URL
    redirect_uri = f'{domain}/auth/api/login/google/'

    code = validated_data.get('code')
    error = validated_data.get('error')

    if error or not code:
        params = urlencode({'error': error})
        return redirect(f'{LOGIN_URL}?{params}')
    
    access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)
    user_data = google_get_user_info(access_token=access_token)

    email_address = user_data['email']
    first_name = user_data.get('given_name')
    last_name = user_data.get('family_name')

    user, created = User.objects.get_or_create(
        username=email_address,
        defaults={
            'firstname': first_name,
            'lastname': last_name,
        }
    )
    
    login(request, user) 
    return user

def apple_get_access_token(code:str,redirect_uri:str) ->str:
    data = {
        'code':code,
        'client_id' :settings.APPLE_CLIENT_ID,
        'client_secret':settings.APPLE_KEY_ID,
        'redirect_uri':redirect_uri,
        'grant_type' :'authorization_code'
    }
    
    response = requests.post('APPLe_ACCESS_TOKEN_OBTAIN_URL',data=data)
    if not response.ok:
        raise ValidationError('Colud not get access token from Apple.')
    
    access_token = response.json()['access_token']
    
    return access_token

def apple_verify_id_token(access_token:str) -> Dict[str,Any]:
    response = requests.get(
        'APPLE_USER_INFO_URL',
        params={'access_token':access_token}
    )
    if not response.ok:
        raise ValidationError('Could not get user info from Apple')
    
    return response.json()

def apple_get_user_data(validated_data,request: HttpRequest):
    domain = settings.BASE_API_URL
    redirect_uri = f'{domain}/auth/api/login/apple/'
    
    code = validated_data.get('code')
    error = validated_data.get('error')
    
    if error or not code:
        params = urlencode({'error':error})
        
    access_token = apple_get_access_token(code=code,redirect_uri=redirect_uri)
    user_data = apple_verify_id_token(access_token=access_token)
    
    email_address = user_data['email']
    first_name = user_data.get('given_name')
    last_name = user_data.get('family_name')
    
    user, created = User.objects.get_or_create(
        username=email_address,
        defaults={
            'firstname':first_name,
            'lastname':last_name,
        }
    )
    
    login(request,user)
    return user