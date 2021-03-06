# -*- coding: utf-8 -*-
import logging
import requests
import time
import vk_api
import platform
import re
import SimpleBot
import templates
from PIL import Image

import ImageCutter

platform_string = ' '.join(platform.uname())
#urllib.urlretrieve(img, "...\img.jpg")
logging.basicConfig(filename='NMM-bot.log', format='[%(asctime)s][%(levelname)s]:%(message)s', level=logging.INFO, datefmt='%d.%m.%Y %H:%M:%S')

logging.info('Started at '+platform_string)
image_path = 'bot_images/'

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
    #print(error_msg)
    logging.error(error_msg)

vk = vk_session.get_api()


def send_vk_message(pid, message, is_chat = False, attachment=None):
    if is_chat:
        vk.messages.send(chat_id=pid, message=message, attachment=attachment)
    else:
        vk.messages.send(user_id=pid, message=message, attachment=attachment)


def send_vk_unified_message(pid, message, is_chat = False):
    att_string_all = None
    if message.has_attachments:
        att_string_all = ''
        for att in message.attachments:
            if att_string_all != '':
                att_string_all += ','
            if att.type == 'photo':
                now_time = int(time.time())
                try:
                    vk_img = upload.photo_messages(att.path)
                    att_string = 'photo' + str(vk_img[0]['owner_id']) + '_' + str(vk_img[0]['id'])
                except vk_api.exceptions.ApiError as error_msg:
                    logging.error('vk_api.exceptions.ApiError: ' + str(error_msg))
                    message.body += '\n[error while uploading photo]'
            att_string_all += att_string
    if is_chat:
        vk.messages.send(chat_id=pid, message=message.body, attachment=att_string_all)
    else:
        vk.messages.send(user_id=pid, message=message.body, attachment=att_string_all)


def work_with_message(message, pid, user_id, is_chat):
    global upload
    global to_work
    sender = SimpleBot.MessageSender({'pid': pid, 'is_chat': is_chat}, send_vk_unified_message)
    logging.debug(message)
    msg = SimpleBot.VkMessage(message)
    if message['body'] == 'exit':
        if user_id in admins:
            send_vk_message(pid, 'exiting...', is_chat)
            logging.info('exiting...')
            to_work = False
        else:
            send_vk_message(pid, 'Ты не мой хозяин, я не буду подчиняться!', is_chat)
    elif 'say my name' in message['body'].lower():
        user_info = vk.users.get(user_ids=str(user_id), fields='maiden_name')
        send_vk_message(pid, 'You are %s %s' % (user_info[0]['first_name'], user_info[0]['last_name']), is_chat)
    elif 'trim twitmeme' in message['body'].lower():
        if 'attachments' in message:
            att_s = message['attachments']
            if len(att_s) > 1:
                send_vk_message(pid, 'только одна пикча, нибба.', is_chat)
            else:
                print(att_s)
                att = att_s[0]
                if att['type'] == 'photo':
                    photo = att['photo']
                    photo_url = '0'
                    for key in ['photo_2560', 'photo_1280', 'photo_807', 'photo_604', 'photo_130', 'photo_75']:
                        if key in photo:
                            photo_url = photo[key]
                            break
                    print(photo_url)
                    ext = '.jpg'
                    if '.png' in photo_url:
                        ext = '.png'
                    now_time = int(time.time())
                    src_name = image_path+'srcimg_'+str(now_time)+ext
                    r = requests.get(photo_url)
                    img_file = open(src_name, 'wb')
                    img_file.write(r.content)
                    img_file.close()
                    pil_img = Image.open(src_name)
                    try:
                        img1, img2 = ImageCutter.SplitTwitterMemeImage(pil_img)
                    except Warning as err:
                        print('Error: ', err)
                        send_vk_message(pid, 'unable to trim :(', is_chat)
                    else:
                        send_vk_message(pid, 'Done! Uploading...', is_chat)
                        img1.save(image_path+'out1_'+str(now_time)+'.png', 'PNG')
                        img2.save(image_path+'out2_'+str(now_time)+'.png', 'PNG')
                        msg = SimpleBot.Message('Here:')
                        msg.add_photo(image_path+'out1_'+str(now_time)+'.png')
                        msg.add_photo(image_path+'out2_'+str(now_time)+'.png')
                        send_vk_unified_message(pid, msg, is_chat)
                else:
                    send_vk_message(pid, 'ИМЕННО ПИКЧА, НИББА', is_chat)
        else:
            send_vk_message(pid, 'Где пикча, нибба?', is_chat)
    else:
        for k in templates.rules_templates.keys():
            if re.search(k, msg.body):
                res = templates.rules_templates[k](msg, sender)

    vk.messages.markAsRead(message_ids=message['id'])


def work_with_private_message(message, user_id):
    print(message)
    vk.messages.markAsRead(message_ids=message['id'])


def work_with_single_dialog(messages_list, dialog):
    #print(dialog)
    for message in messages_list:
        if not (message['read_state']) and ((message.get('user_id') == dialog['id']) or (message.get('chat_id') == dialog['id'])):
            #print('m', message)
            work_with_message(message, dialog['id'], dialog['user_id'], dialog['is_chat'])


def work_with_msg(dialogs):
    global to_work
    #print('NEW MESSAGS')
    logging.info('New messages:')
    count = 3
    dialogs_to_work = []
    for d_n, dialog in enumerate(dialogs):
        message = dialog['message']
        count += dialog['unread']
        user_info = vk.users.get(user_ids=str(message['user_id']), fields='maiden_name')
        if 'chat_id' in message:
            dialogs_to_work.append({'is_chat': True, 'id': message['chat_id'], 'user_id': message['user_id'], 'chat_id': message['chat_id'], 'unread': dialog['unread']})
            logging.info('%d unread messages from chat "%s" (chat_id %d) from user %s %s (user_id %d). Last message: "%s"' % (dialog['unread'], message['title'], message['chat_id'], user_info[0]['first_name'], user_info[0]['last_name'], message['user_id'], message['body']))
            #print('Из беседы "%s" (id беседы %d) %d непрочитанных сообщений. Последнее сообщение: "%s"' % (message['title'], message['chat_id'], dialog['unread'], message['body']))
        else:
            dialogs_to_work.append({'is_chat': False, 'id': message['user_id'], 'user_id': message['user_id'], 'unread': dialog['unread']})
            logging.info('%d unread messages from %s %s (user_id %d). Last message: "%s"' % (dialog['unread'], user_info[0]['first_name'], user_info[0]['last_name'], message['user_id'], message['body']))
            #print('От пользователя с id %d %d сообщений. Последнее сообщение: "%s"' % (message['user_id'], dialog['unread'], message['body']))
    messages = vk.messages.get(count=count)
    for dialog in dialogs_to_work:
        #print(dialog)
        work_with_single_dialog(messages['items'], dialog)


def main():
    global upload
    global to_work
    for uid in admins:
        if False:
            send_vk_message(uid, 'Bot started at platform '+platform_string, False)
    while to_work:
        dialogs = vk.messages.getDialogs(unread=1)
        #print(dialogs)
        if dialogs['count']:
            work_with_msg(dialogs['items'])
        time.sleep(0.1)
    for uid in admins:
        send_vk_message(uid, 'Bot stopped', False)


main()
