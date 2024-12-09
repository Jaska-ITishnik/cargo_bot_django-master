import requests

arrived = {
    'uz': "Buyurtmangiz O'zbekistonga yetib keldi!\nTovar trek kodi: {0}\nTovar nomi: {1}\nTovar kg: {2}\nKub kg: {3}\nTo'lov: {4}\n\n"
          "Siz tovarlaringizni quyidagi manzildan olishingiz mumkin:\n"
          "{5}",
    'ru': "Ваш заказ прибыл в Узбекистан!\nТрек-код товара: {0}\nНазвание товара: {1}\nТовар кг: {2}\nКуб кг: {3}\nОплата: {4}\n\n"
          "Вы можете забрать свой товар по следующему адресу:\n"
          "{5}"
}

arrived_china = {
    'uz': "Buyurtmangiz Xitoy skladimizga yetib keldi!\nTovar trek kodi: {0}\nTovar nomi: {1}\nTovar kg: {2}\nKub kg: {3}",
    'ru': "Ваш заказ прибыл в Узбекистан!\nТрек-код товара: {0}\nНазвание товара: {1}\nТовар кг: {2}\nКуб кг: {3}"
}

taken_order = {
    'uz': "{0} -> trek kodliy maxsulotni qabul qildingiz🤝",
    'ru': "Вы получили товар с кодом -> {0} 🤝",
}


def send_telegram_notification(text, chat_id, photo_path=None):
    token = '7139094213:AAF1g3Gmfk0Zt1ERV-XolSATn5fqEoPYI_E'
    # token = '7510074118:AAGiuncdv44_TFuvmeJ-vekE4yRwuDx9LcI'
    base_url = f'https://api.telegram.org/bot{token}/'

    if photo_path:
        url = base_url + 'sendPhoto'
        with open(photo_path, 'rb') as photo:
            response = requests.post(url, data={'chat_id': chat_id, 'caption': text}, files={'photo': photo})
    else:
        url = base_url + 'sendMessage'
        response = requests.get(url, params={'chat_id': chat_id, 'text': text})
