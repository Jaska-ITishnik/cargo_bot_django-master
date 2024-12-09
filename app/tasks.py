from celery import shared_task

from app.models import Address, Product
from utils import send_telegram_notification, arrived


@shared_task
def send_daily_notifications():
    print('Triggered send_notification!')
    uzbek_address_uz = Address.objects.all().last().address_uzbek_uz
    uzbek_address_ru = Address.objects.all().last().address_uzbek_ru
    products = Product.objects.filter(is_taken=False, is_arrived=True)
    for product in products:
        user = product.user
        if user:
            address = (
                    product.user.lang == 'uz'
                    and uzbek_address_uz
                    or uzbek_address_ru
            )
            notification_text = arrived[user.lang].format(
                product.trek_code, product.name, product.own_kg,
                product.standart_kg, product.summary, address
            )
            if product.image:
                send_telegram_notification(notification_text, user.tg_id, product.image.path)
            else:
                send_telegram_notification(notification_text, user.tg_id)
