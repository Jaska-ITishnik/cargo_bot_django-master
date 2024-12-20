from app.models import Product
from app.product_manager import NotRegisteredUserManager


class NotRegisteredProductProxy(Product):
    objects = NotRegisteredUserManager()

    class Meta:
        proxy = True
        verbose_name = "Egasi yo'q tovar"
        verbose_name_plural = "Egasi yo'q tovarlar"
