# -*- coding: utf-8 -*-
import random
import time
import vk_api

admins = [216726992, 169295669]

to_work = True
f = open('login_data.txt', 'r')
app_id, login, password = f.readline().split(':')
f.close()
password = password.split('\n')[0]
vk_session = vk_api.VkApi(login, password, app_id=app_id)
upload = vk_api.VkUpload(vk_session)

try:
    vk_session.auth()
except vk_api.AuthError as error_msg:
    print(error_msg)

vk = vk_session.get_api()

now_time = time.time()
start_time = int(now_time)-int(now_time) % 86400 - 86400
end_time = int(now_time)-int(now_time) % 86400
news = vk.newsfeed.get(filters='posts', source_ids='list{1}', start_time=start_time, end_time=end_time)
print(news.keys())
items = news['items']
while news.get('next_from'):
    news = vk.newsfeed.get(filters='posts', source_ids='list{1}', start_time=start_time, end_time=end_time, start_from = news['next_from'])
    print(news.keys())
    items += news['items']
posts = []
print(len(items))
for post in items:
    if post['type'] == 'post':
        if 'attachments' in post.keys():
            ph = 0
            for i in post['attachments']:
                if i['type'] == 'photo':
                    ph += 1
            if ph == 1:
                posts.append(post)
print(len(posts))
post = posts[random.randint(0, len(posts))]
print(post['attachments'][0]['photo'])
