import requests

arrived = {
    'uz': "Buyurtmangiz O'zbekistonga yetib keldi!\nTovar trek kodi: {0}\nTovar nomi: {1}\nTovar kg: {2}\nKub kg: {3}\nDaofusi: {5}\nTo'lov: ${4}\n\n"
          "Siz tovarlaringizni quyidagi manzildan olishingiz mumkin:\n"
          "{6}",
    'ru': "Ваш заказ прибыл в Узбекистан!\nТрек-код товара: {0}\nНазвание товара: {1}\nТовар кг: {2}\nКуб кг: {3}\nDaofu: {5}\nОплата: ${4}\n\n"
          "Вы можете забрать свой товар по следующему адресу:\n"
          "{6}",
    'en': "Your order has arrived in Uzbekistan!\nProduct tracking code: {0}\nProduct name: {1}\nProduct weight: {2}\nCubic weight: {3}\nDaofu: {5}\nPayment: ${4}\n\n"
          "You can pick up your items at the following address:\n"
          "{6}",
    'zh': "您的订单已到达乌兹别克斯坦！\n商品追踪码: {0}\n商品名称: {1}\n商品重量: {2}\n立方重量: {3}\n到达付款: {5}\n付款: ${4}\n\n"
          "您可以在以下地址领取您的商品:\n"
          "{6}"
}

arrived_china = {
    'uz': "Buyurtmangiz Xitoy skladimizga yetib keldi!\nTovar trek kodi: {0}\nTovar nomi: {1}\nTovar kg: {2}\nKub kg: {3}",
    'ru': "Ваш заказ прибыл на наш склад в Китае!\nТрек-код товара: {0}\nНазвание товара: {1}\nТовар кг: {2}\nКуб кг: {3}",
    'en': "Your order has arrived at our warehouse in China!\nProduct tracking code: {0}\nProduct name: {1}\nProduct weight: {2}\nCubic weight: {3}",
    'zh': "您的订单已到达我们在中国的仓库！\n商品追踪码: {0}\n商品名称: {1}\n商品重量: {2}\n立方重量: {3}"
}

taken_order = {
    'uz': "{0} -> trek kodli maxsulotni qabul qildingiz\nFad kargoni tanlaganingiz uchun raxmat😊",
    'ru': "Вы получили товар с кодом -> {0}\nБлагодарим вас за выбор Fad Cargo😊",
    'en': "You have received the product with tracking code -> {0}\nThank you for choosing Fad Cargo😊",
    'zh': "您已收到追踪码为 -> {0} 的商品\n感谢您选择Fad Cargo😊"
}


def send_telegram_notification(text, chat_id, photo_path=None):
    # token = '7139094213:AAF1g3Gmfk0Zt1ERV-XolSATn5fqEoPYI_E'
    token = '7510074118:AAGiuncdv44_TFuvmeJ-vekE4yRwuDx9LcI'
    base_url = f'https://api.telegram.org/bot{token}/'

    if photo_path:
        url = base_url + 'sendPhoto'
        with open(photo_path, 'rb') as photo:
            response = requests.post(url, data={'chat_id': chat_id, 'caption': text}, files={'photo': photo})
    else:
        url = base_url + 'sendMessage'
        response = requests.get(url, params={'chat_id': chat_id, 'text': text})
