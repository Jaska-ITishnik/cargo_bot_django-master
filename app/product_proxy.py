from app.models import Product
from app.product_manager import NotRegisteredUserManager
from django.utils.translation import gettext_lazy as _

class NotRegisteredProductProxy(Product):
    objects = NotRegisteredUserManager()

    class Meta:
        proxy = True
        verbose_name = _("Egasi yo'q tovar")
        verbose_name_plural = _("Egasi yo'q tovarlar")
