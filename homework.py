import time
import os

import requests
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('VK_TOKEN')
acc_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
number_from = os.getenv('NUMBER_FROM')
number_to = os.getenv('NUMBER_TO')


def get_status(user_id):
    params = {
        'user_ids' : user_id,
        'fields' : 'online',
        'v' : 5.92,
        'access_token' : token,
    }
    user_status = requests.post('https://api.vk.com/method/users.get', params=params).json()['response'][0]['online']
    return user_status  # Верните статус пользователя в ВК


def sms_sender(sms_text):
    client = Client(acc_sid, auth_token)
    message = client.messages.create(
        body=sms_text,
        from_=number_from,
        to=number_to
    )
    return message.sid  # Верните sid отправленного сообщения из Twilio


if __name__ == "__main__":
    vk_id = input("Введите id: ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
