from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import logout
import json
import requests

def logout_view(request):
    logout(request)
    return render(request,'index.html')


def index(request):
    if request.user.is_authenticated:
        return logined(request)
    else:
        return render(request,'index.html')


def logined(request):
    user = request.user
    social = user.social_auth.get(provider='vk-oauth2')
    response = requests.get(
        'https://api.vk.com/method/friends.get',
        params={'order': 'random',
                'fields': ('nickname'),
                'count': '5',
                'access_token': social.extra_data['access_token'],
                'v': '5.101'}
    )
    try:
        friend_list = response.json()['response']['items']
    except KeyError:
        return logout_view(request)

    friend_name_list = []
    for friend in friend_list:
        friend_name_list.append('{0} {1}'.format(str(friend['first_name']), str(friend['last_name'])))

    return render(request, 'logined.html', {'friend_name': friend_name_list, 'first_name': request.user.first_name,
                                            'last_name': request.user.last_name})
