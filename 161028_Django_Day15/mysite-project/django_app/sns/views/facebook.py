import json
from collections import Counter

import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from apis import facebook

__all__ = [
    'friends_ranking',
]


def friends_ranking(request):
    if request.method == 'GET':
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
            # print(json_data)

            comment_list = []
            # data의 각 item이 feed
            for feed in dict_feed_info.get('data'):
                if feed.get('comments'):
                    for comment in feed.get('comments').get('data'):
                        comment_list.append(comment)

            # print(comment_list)

            counter = Counter()
            id_list = [comment.get('from', {}).get('id') for comment in comment_list]
            for id in id_list:
                counter[id] += 1

            # print(counter)
            most_list = counter.most_common()
            req_id_list = list(set(id_list))
            print(req_id_list)
            str_req_id_list = ','.join(req_id_list)
            print(str_req_id_list)

            uri_request_user_info_list = 'https://graph.facebook.com/v2.8/?ids={ids}&' \
                                         'fields=cover,email,picture.width(500).height(500),name&' \
                                         'access_token={access_token}'.format(
                                            ids=str_req_id_list,
                                            access_token=access_token
                                        )

            r = requests.get(uri_request_user_info_list)
            dict_friends_info = r.json()
            json_friends_info = json.dumps(dict_friends_info, indent=2)
            print(json_friends_info)

            most_dict_list = []
            for item in most_list:
                id = item[0]
                for k in dict_friends_info:
                    if k == id and k != user_id:
                        most_dict_list.append({
                            'info': dict_friends_info[k],
                            'number': item[1]
                        })

            context = {
                'most_dict_list': most_dict_list
            }
            return render(request, 'sns/facebook/friends_ranking.html', context)
    elif request.method == 'POST':
        import ast
        str_item_list = request.POST.getlist('item')

        for str_item in str_item_list:
            item = ast.literal_eval(str_item)
            print(item)
