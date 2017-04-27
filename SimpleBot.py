import time
import requests


class attachment(object):
    def __init__(self, path):
        self.path = path
        self.type = 'base'


class photo(attachment):
    def __init__(self, photo_path):
        super().__init__(photo_path)
        self.type = 'photo'


class MessageSender(object):
    def __init__(self, data, func):
        self.__data = data
        self.__sender_func = func

    def update_data(self, data):
        self.__data = data

    def send(self, message):
        self.__sender_func(**self.__data, message=message)

class Message(object):
    def __init__(self, body, attachments=None):
        self.body = body
        self.attachments = []
        self.has_attachments = False
        if attachments:
            self.has_attachments = True
            for i in range(len(attachments)):
                try:
                    super(attachment, attachments[i])
                except TypeError:
                    pass
                else:
                    self.attachments.append(attachments[i])

    def add_photo(self, path):
        self.has_attachments = True
        self.attachments.append(photo(path))


class VkMessage(Message):
    def __init__(self, vkmsg):
        body = vkmsg['body']
        if 'attachments' in vkmsg:
            attachments = []
            for att in vkmsg['attachments']:
                if att['type'] == 'photo':
                    vk_att_photo = att['photo']
                    photo_url = '0'
                    for key in ['photo_2560', 'photo_1280', 'photo_807', 'photo_604', 'photo_130', 'photo_75']:
                        if key in vk_att_photo:
                            photo_url = vk_att_photo[key]
                            break
                    print(photo_url)
                    ext = '.jpg'
                    if '.png' in photo_url:
                        ext = '.png'
                    r = requests.get(photo_url)
                    now_time = int(time.time())
                    src_name = 'attachments/' + 'srcimg_' + str(now_time) + ext
                    img_file = open(src_name, 'wb')
                    img_file.write(r.content)
                    img_file.close()
                    att_photo = photo(src_name)
                    attachments.append(att_photo)
            super().__init__(body, attachments=attachments)
        else:
            super().__init__(body)
