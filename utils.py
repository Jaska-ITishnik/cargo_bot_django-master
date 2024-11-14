import requests

arrived = {
    'uz': "Buyurtmangiz O'zbekistonga yetib keldi!\nTovar trek kodi: {0}\nTovar nomi: {1}\nTovar kg: {2}\nKub kg: {3}\nTo'lov: {4}\n\n"
          "Siz tovarlaringizni quyidagi manzildan olishingiz mumkin:\nToshkent shahar,Shayxontohur "
          "tumani,Kichik halqa yo’li, 147  2-qavat",
    'ru': "Ваш заказ прибыл в Узбекистан!\nТрек-код товара: {0}\nНазвание товара: {1}\nТовар кг: {2}\nКуб кг: {3}\nОплата: {4}\n\n"
          "Вы можете забрать свой товар по следующему адресу: г.Ташкент, Шайхонтохур"
          "Район, Малая кольцевая дорога, 147 2-этаж"
}

arrived_china = {
    'uz': "Buyurtmangiz Xitoy skladimizga yetib keldi!\nTovar trek kodi: {0}\nTovar nomi: {1}\nTovar kg: {2}\nKub kg: {3}",
    'ru': "Ваш заказ прибыл в Узбекистан!\nТрек-код товара: {0}\nНазвание товара: {1}\nТовар кг: {2}\nКуб кг: {3}"
}


def send_telegram_notification(text, chat_id):
    token = '7139094213:AAF1g3Gmfk0Zt1ERV-XolSATn5fqEoPYI_E'
    url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id='
    requests.get(url + str(chat_id) + '&text=' + text)
