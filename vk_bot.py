import vk_api, time, requests
from PIL import Image
import ImageCutter
#urllib.urlretrieve(img, "...\img.jpg")

image_path = 'bot_images/'

admin = 216726992

to_work = True


def work_with_chat_message(message, chat_id, vk):
    global upload
    print(message)
    if message['body'] == 'bot':
        vk.messages.send(chat_id=chat_id, message='Yes my lord')
    elif ('spell i🅱up' in message['body'].lower()) or ('spell icup' in message['body'].lower()):
        vk.messages.send(chat_id=chat_id, message='HOLD THE MAYO')
    elif message['body'] == 'обрежь твитмем':
        if 'attachments' in message:
            att_s = message['attachments']
            if len(att_s) > 1:
                vk.messages.send(chat_id=chat_id, message='только одна пикча, нибба.')
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
                        vk.messages.send(chat_id=chat_id, message='не режется :(')
                    else:
                        img1.save(image_path+'out1_'+str(now_time)+'.png', 'PNG')
                        img2.save(image_path+'out2_'+str(now_time)+'.png', 'PNG')
                        vk_img1 = upload.photo_messages(image_path+'out1_'+str(now_time)+'.png')
                        vk_img2 = upload.photo_messages(image_path+'out2_'+str(now_time)+'.png')
                        vk.messages.send(chat_id=chat_id, message='ГОТОВО!!!', attachment='photo'+str(vk_img1[0]['owner_id'])+'_'+str(vk_img1[0]['id'])+','+'photo'+str(vk_img2[0]['owner_id'])+'_'+str(vk_img2[0]['id']))
                else:
                    vk.messages.send(chat_id=chat_id, message='ИМЕННО ПИКЧА, НИББА')
        else:
            vk.messages.send(chat_id=chat_id, message='Где пикча, нибба?')
    vk.messages.markAsRead(message_ids=message['id'])


def work_with_private_message(message, user_id, vk):
    print(message)
    vk.messages.markAsRead(message_ids=message['id'])


def work_with_single_dialog(messages_list, dialog, vk):
    #print(dialog)
    if dialog['is_chat']:
        for message in messages_list:
            if not (message['read_state']) and message['chat_id'] == dialog['chat_id']:
                #print('m', message)
                work_with_chat_message(message, dialog['chat_id'], vk)
    else:
        for message in messages_list:
            if not (message['read_state']) and message['user_id'] == dialog['user_id']:
                #print('m', message)
                work_with_private_message(message, dialog['user_id'], vk)


def work_with_msg(dialogs, vk):
    global to_work
    print('NEW MESSAGS')
    count = 3
    dialogs_to_work = []
    for d_n, dialog in enumerate(dialogs):
        message = dialog['message']
        count += dialog['unread']
        if 'chat_id' in message:
            dialogs_to_work.append({'is_chat': True, 'chat_id': message['chat_id'], 'unread': dialog['unread']})
            print('Из беседы "%s" (id беседы %d) %d непрочитанных сообщений. Последнее сообщение: "%s"' % (message['title'], message['chat_id'], dialog['unread'], message['body']))
        else:
            dialogs_to_work.append({'is_chat': False, 'user_id': message['user_id'], 'unread': dialog['unread']})
            if message['user_id'] == admin and message['body'] == 'exit':
                to_work = False
            print('От пользователя с id %d %d сообщений. Последнее сообщение: "%s"' % (message['user_id'], dialog['unread'], message['body']))
    messages = vk.messages.get(count=count)
    for dialog in dialogs_to_work:
        work_with_single_dialog(messages['items'], dialog, vk)




def main():
    global upload
    global to_work
    f = open('login_data.txt', 'r')
    app_id, login, password = f.readline().split(':')
    f.close()
    vk_session = vk_api.VkApi(login, password)
    upload = vk_api.VkUpload(vk_session)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    while to_work:
        dialogs = vk.messages.getDialogs(unread=1)
        #print(dialogs)
        if dialogs['count']:
            work_with_msg(dialogs['items'], vk)
        time.sleep(0.5)


main()
