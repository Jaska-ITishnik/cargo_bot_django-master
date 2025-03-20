import os
from decimal import Decimal

from django.db import models
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

# Create your models here.


LANGUAGE = (
    ('uz', "Uzbek"),
    ('ru', "Russian"),
    ('en', "English"),
    ('zh', "Chinese")
)

CONSIGNMENT = (
    ('Birinchi', 'Birinchi'),
    ('Ikkinchi', 'Ikkinchi'),
    ('Uchinchi', 'Uchinchi'),
)

TYPES = (
    ("A", "A"),
    ("B", "B"),
    ("C", "C"),
)
load_dotenv()


class User(models.Model):
    full_name = models.CharField(max_length=255, null=True, verbose_name=_("To'liq ismi"))
    phone_number = models.CharField(max_length=255, null=True, verbose_name=_("Telefon raqam"))
    phone_number2 = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Telefon raqam 2"))
    lang = models.CharField(max_length=2, choices=LANGUAGE, default="uz", null=True, verbose_name=_("Til"))
    passport1 = models.ImageField(upload_to='users/passports', null=True, verbose_name=_("Passport old tomoni"))
    passport2 = models.ImageField(upload_to='users/passports', null=True, verbose_name=_("Passport orqa tomoni"))
    latitude = models.FloatField(null=True)  #
    longitude = models.FloatField(null=True)  #
    id_code = models.CharField(max_length=255, null=True, verbose_name=_("ID kod"))
    is_active = models.BooleanField(default=False, null=True)  #
    tg_id = models.PositiveBigIntegerField(null=True)  #
    image = models.ImageField(upload_to='users/image', null=True, verbose_name=_("Rasm"))
    is_standart = models.BooleanField(default=False, null=True, verbose_name=_("Standart mi?"))
    is_kg = models.BooleanField(default=False, null=True, verbose_name=_("Kg mi?"))
    default_price = models.DecimalField(blank=True, null=True, max_digits=15, decimal_places=2,
                                        verbose_name=_("Maxsus narx"))
    referal = models.ForeignKey('Referal', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Реферал"))
    types = models.CharField(choices=TYPES, default="A", max_length=1, verbose_name=_('Tip'))

    def __str__(self):
        return self.id_code or "Not full user"

    def save(self, *args, **kwargs):
        products = self.products.all()
        for product in products:
            if self.default_price:
                product.summary = self.default_price
            elif self.is_standart:
                product.summary = (
                                          product.stan_kg * product.service_price) + product.daofu / product.consignment.yuan_dollar
            else:
                self.summary = (
                                       product.own_kg * product.service_price) + product.daofu / product.consignment.yuan_dollar
            product.save()
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Foydalanuvchi")
        verbose_name_plural = _("Foydalanuvchilar")
        db_table = 'users'


class CreatedAt(models.Model):
    batch_name = CharField(max_length=50, null=True, blank=True, unique=True, verbose_name=_("Partiya nomi"))
    date = models.DateField(verbose_name=_("Sana"))
    consignment = models.CharField(max_length=15, choices=CONSIGNMENT, default="Birinchi", verbose_name=_("Partiya"))
    expenses = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=_("Xarajatlar"))
    transport_expenses = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                             verbose_name=_("Transport xarajatlar"))
    tax = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=_("Naloglar"))
    add_expenses = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                       verbose_name=_("Qo'shimcha xarajatlar"))
    kg = models.DecimalField(max_digits=15, decimal_places=2,
                             verbose_name=_("KG"))
    from_who = models.CharField(max_length=255, verbose_name=_("Kimdan"))
    to_who = models.CharField(max_length=255, verbose_name=_("Kimga"))
    yuan_dollar = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("Yuan Dollar"))
    dollar_sum = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("Dollar Sum"))

    def __str__(self):
        return f"{self.date} -> {self.consignment}"

    class Meta:
        verbose_name = _("Partiya")
        verbose_name_plural = _("Partiyalar")
        db_table = 'created_at'


class Product(models.Model):
    consignment = models.ForeignKey(CreatedAt, on_delete=models.CASCADE, related_name='products',
                                    verbose_name=_("Partiya"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', verbose_name=_("Egasi"),
                             null=True,
                             blank=True)
    unregistered_user_phone = CharField(max_length=20, null=True, blank=True,
                                        verbose_name=_("register bo'lmagan"))
    trek_code = models.CharField(max_length=255, null=True, verbose_name=_("Trek kod"))
    name = models.CharField(max_length=255, null=True, verbose_name=_("Nomi"), blank=True)
    quantity = models.PositiveBigIntegerField(verbose_name=_("Soni"), null=True, blank=True)
    tall = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("Uzunlik"), null=True, blank=True)
    width = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("Kenglik"), null=True, blank=True)
    height = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("Balanglik"), null=True, blank=True)
    # (boyi * eni * balandligi) / 6000
    standart_kg = models.DecimalField(max_digits=15, decimal_places=2,
                                      verbose_name=_("Standart kg"))
    own_kg = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("Og'irligi"))
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("Tovar narxi"))
    service_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("Xizmat narxi"))
    summary = models.DecimalField(max_digits=15, decimal_places=2, null=True, verbose_name=_("Umumiy"), blank=True,
                                  default=0.00)
    is_arrived = models.BooleanField(default=False, verbose_name=_("Uzb ga kelganmi?"), null=True, blank=True)
    is_taken = models.BooleanField(default=False, verbose_name=_("Klientni qolidami?"), null=True, blank=True)
    is_china = models.BooleanField(default=False, verbose_name=_("Xitoy skladidami?"), null=True, blank=True)
    image = models.ImageField(upload_to='products', null=True, blank=True, verbose_name=_("Rasm"))
    daofu = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("Daofu"), null=True, blank=True,
                                default=0.00)

    def save(self, *args, **kwargs):
        if all(
                value in [None, "", 0]
                for value in [self.user, self.unregistered_user_phone, self.trek_code,
                              self.name, self.quantity, self.tall, self.width, self.height,
                              self.standart_kg, self.own_kg, self.price, self.service_price, self.summary,
                              self.is_china, self.is_arrived, self.is_taken, self.daofu]
        ):
            return
        stan_kg = 0
        if self.tall and self.width and self.height:
            stan_kg = (self.tall * self.width * self.height) / 6000
            self.standart_kg = stan_kg
        if self.user:
            if self.user.default_price:
                self.summary = self.user.default_price
            elif self.user.is_standart and self.service_price and self.daofu:
                self.summary = Decimal(stan_kg * self.service_price) + Decimal(self.daofu) / Decimal(
                    self.consignment.yuan_dollar)
        if self.own_kg and self.service_price and self.daofu:
            self.summary = Decimal(self.own_kg * self.service_price) + Decimal(self.daofu) / Decimal(
                self.consignment.yuan_dollar)
        else:
            self.summary = Decimal(self.own_kg * self.service_price)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        if self.user and self.name:
            return self.user.full_name + " -> " + self.name
        return str(self.trek_code)  #

    @property
    def Xizmat_narxi(self):
        return f"💲{self.service_price}"

    @property
    def dafousi(self):
        return f"¥{self.daofu}"

    class Meta:
        verbose_name = _("Tovar")
        verbose_name_plural = _("Tovarlar")
        db_table = 'products'


class Referal(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Nomi"))
    quantity = models.PositiveBigIntegerField(default=0, verbose_name=_("Soni"))
    link = models.URLField(max_length=255, null=True, blank=True, verbose_name=_("Ссылка"))

    class Meta:
        verbose_name = _("Referal")
        verbose_name_plural = _("Referallar")
        db_table = 'referal'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        bot = os.getenv("BOT_USERNAME")
        self.link = f"https://t.me/{bot}?start={self.name}"
        super(Referal, self).save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Kimdan"))
    comment = models.TextField(verbose_name=_("Izoh"))

    class Meta:
        verbose_name = _("Izoh")
        verbose_name_plural = _("Izohlar")
        db_table = 'comments'


class Phones(models.Model):
    phone = models.CharField(max_length=13, verbose_name=_('Telefon raqam'),
                             help_text=_("Plus belgisi bilan jami 13 ta belgi bolishi kerak"))

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = _("Telefon")
        verbose_name_plural = _("Telefonlar")
        db_table = 'phones'


class ActivePhone(models.Model):
    phone = models.ForeignKey(Phones, on_delete=models.CASCADE, verbose_name=_("Aktiv telefon"))

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = _("Aktiv telefon")
        verbose_name_plural = _("Aktiv telefon")
        db_table = 'active_phones'


class Address(models.Model):
    period_avia = CharField(max_length=20, default='1-15')
    period_avto = CharField(max_length=20, default='15-30')
    phone_number = CharField(max_length=30, default='17800293735')
    mail_address = CharField(max_length=30, default='100024')
    address = CharField(max_length=255, default='北京市朝阳区定福景园7号楼3单元1002 17800293735')
    address_uzbek_uz = CharField(max_length=255,
                                 default='Toshkent shahar,Shayxontohur tumani,Kichik halqa yo’li, 147  5-qavat',
                                 verbose_name=_("O'zbekiston manzili 🇺🇿"))
    address_uzbek_ru = CharField(max_length=255,
                                 default='г. Ташкент, Шайхонтохурский район, Малая кольцевая дорога, 147, 5 этаж',
                                 verbose_name=_("O'zbekiston manzili 🇷🇺"))

    class Meta:
        verbose_name = _('Manzil')
        verbose_name_plural = _('Manzillar')
