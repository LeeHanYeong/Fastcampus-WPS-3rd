import requests
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from member.apis import facebook

__all__ = [
    'friends_ranking',
]


def friends_ranking(request):
    if request.GET.get('error'):
        return HttpResponse('사용자 로그인 거부')
    if request.GET.get('code'):
        redirect_uri = 'http://{host}{url}'.format(
            host=request.META['HTTP_HOST'],
            url=reverse('sns:friends_ranking')
        )
        print('redirect_uri : %s' % redirect_uri)
        code = request.GET.get('code')
        access_token = facebook.get_access_token(code, redirect_uri)
        user_id = facebook.get_user_id_from_token(access_token)

        url_request_feed = 'https://graph.facebook.com/v2.8/{user_id}/feed?' \
                           'fields=comments{{from,comments}}&' \
                           'access_token={access_token}'.format(
                                user_id=user_id,
                                access_token=access_token,
                            )

        r = requests.get(url_request_feed)
        dict_feed_info = r.json()
        json_data = json.dumps(dict_feed_info, indent=2)
        print(json_data)

        return HttpResponse(json_data)