import os

from django.db import models
from django.db.models import CharField
from dotenv import load_dotenv
from odf.xforms import Model

# Create your models here.


LANGUAGE = (
    ('uz', "Uzbek"),
    ('ru', "Russian")
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
    full_name = models.CharField(max_length=255, null=True, verbose_name="To'liq ismi")
    phone_number = models.CharField(max_length=255, null=True, verbose_name="Telefon raqam")
    phone_number2 = models.CharField(max_length=255, null=True, blank=True, verbose_name="Telefon raqam 2")
    lang = models.CharField(max_length=2, choices=LANGUAGE, default="uz", null=True, verbose_name="Til")
    passport1 = models.ImageField(upload_to='users/passports', null=True, verbose_name="Passport old tomoni")
    passport2 = models.ImageField(upload_to='users/passports', null=True, verbose_name="Passport orqa tomoni")
    latitude = models.FloatField(null=True)  #
    longitude = models.FloatField(null=True)  #
    id_code = models.CharField(max_length=255, null=True, verbose_name="ID kod")
    is_active = models.BooleanField(default=False, null=True)  #
    tg_id = models.PositiveBigIntegerField(null=True)  #
    image = models.ImageField(upload_to='users/image', null=True, verbose_name="Rasm")
    is_standart = models.BooleanField(default=False, null=True, verbose_name="Standart mi?")
    is_kg = models.BooleanField(default=False, null=True, verbose_name="Kg mi?")
    default_price = models.DecimalField(blank=True, null=True, max_digits=15, decimal_places=2,
                                        verbose_name="Maxsus narx")
    referal = models.ForeignKey('Referal', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Реферал")
    types = models.CharField(choices=TYPES, default="A", max_length=1, verbose_name='Tip')

    def __str__(self):
        return self.id_code or "Not full user"

    def save(self, *args, **kwargs):
        products = self.products.all()
        for product in products:
            if self.default_price:
                product.summary = self.default_price
            elif self.is_standart:
                product.summary = (product.stan_kg * product.service_price) + product.daofu
            else:
                self.summary = (product.own_kg * product.service_price) + product.daofu
            product.save()
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        db_table = 'users'


class CreatedAt(models.Model):
    date = models.DateField(verbose_name="Sana")
    consignment = models.CharField(max_length=15, choices=CONSIGNMENT, default="Birinchi", verbose_name="Partiya")
    expenses = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Xarajatlar")
    transport_expenses = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                             verbose_name="Transport xarajatlar")
    tax = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Naloglar")
    add_expenses = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Qo'shimcha xarajatlar")
    kg = models.DecimalField(max_digits=15, decimal_places=2,
                             verbose_name="KG")
    from_who = models.CharField(max_length=255, verbose_name="Kimdan")
    to_who = models.CharField(max_length=255, verbose_name="Kimga")
    yuan_dollar = models.DecimalField(max_digits=15, decimal_places=2)
    dollar_sum = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.date} -> {self.consignment}"

    class Meta:
        verbose_name = "Partiya"
        verbose_name_plural = "Partiyalar"
        db_table = 'created_at'


class Product(models.Model):
    consignment = models.ForeignKey(CreatedAt, on_delete=models.CASCADE, related_name='products',
                                    verbose_name="Partiya")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', verbose_name="Egasi")
    trek_code = models.CharField(max_length=255, null=True, verbose_name="Trek kod")
    name = models.CharField(max_length=255, null=True, verbose_name="Nomi", blank=True)
    quantity = models.PositiveBigIntegerField(verbose_name="Soni", null=True, blank=True)
    tall = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Uzunlik", null=True, blank=True)
    width = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Kenglik", null=True, blank=True)
    height = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Balanglik", null=True, blank=True)
    # (boyi * eni * balandligi) / 6000
    standart_kg = models.DecimalField(blank=True, null=True, max_digits=15, decimal_places=2,
                                      verbose_name="Standart kg")
    own_kg = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Og'irligi")
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Tovar narxi")
    service_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Xizmat narxi")
    summary = models.DecimalField(max_digits=15, decimal_places=2, null=True, verbose_name="Umumiy", blank=True)
    is_arrived = models.BooleanField(default=False, verbose_name="Uzb ga kelganmi?", null=True, blank=True)
    is_taken = models.BooleanField(default=False, verbose_name="Klientni qolidami?", null=True, blank=True)
    is_china = models.BooleanField(default=False, verbose_name="Xitoy skladidami?", null=True, blank=True)
    image = models.ImageField(upload_to='products', null=True, blank=True, verbose_name="Rasm")
    daofu = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Daofu", null=True, blank=True)

    def save(self, *args, **kwargs):
        stan_kg = 0
        if self.tall and self.width and self.height:
            stan_kg = (self.tall * self.width * self.height) / 6000
            self.standart_kg = stan_kg
        if self.user:
            if self.user.default_price:
                self.summary = self.user.default_price
            elif self.user.is_standart and self.service_price and self.daofu:
                self.summary = (stan_kg * self.service_price) + self.daofu
            else:
                if self.own_kg and self.service_price and self.daofu:
                    self.summary = (self.own_kg * self.service_price) + self.daofu
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        if self.user and self.name:
            return self.user.full_name + " -> " + self.name
        return self.trek_code

    class Meta:
        verbose_name = "Tovar"
        verbose_name_plural = "Tovarlar"
        db_table = 'products'


class Referal(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Nomi")
    quantity = models.PositiveBigIntegerField(default=0, verbose_name="Soni")
    link = models.URLField(max_length=255, null=True, blank=True, verbose_name="Ссылка")

    class Meta:
        verbose_name = "Referal"
        verbose_name_plural = "Referallar"
        db_table = 'referal'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        bot = os.getenv("BOT_USERNAME")
        self.link = f"https://t.me/{bot}?start={self.name}"
        super(Referal, self).save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Kimdan")
    comment = models.TextField(verbose_name="Izoh")

    class Meta:
        verbose_name = "Izoh"
        verbose_name_plural = "Izohlar"
        db_table = 'comments'


class Phones(models.Model):
    phone = models.CharField(max_length=13, verbose_name='Telefon raqam',
                             help_text="Plus belgisi bilan jami 13 ta belgi bolishi kerak")

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = "Telefon"
        verbose_name_plural = "Telefonlar"
        db_table = 'phones'


class ActivePhone(models.Model):
    phone = models.ForeignKey(Phones, on_delete=models.CASCADE, verbose_name="Aktiv telefon")

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = "Aktiv telefon"
        verbose_name_plural = "Aktiv telefon"
        db_table = 'active_phones'

class Address(models.Model):
    period_avia = CharField(max_length=20, default='1-15')
    period_avto = CharField(max_length=20, default='15-30')
    phone_number = CharField(max_length=30, default='17800293735')
    mail_address = CharField(max_length=30, default='100024')
    address = CharField(max_length=255, default='北京市朝阳区定福景园7号楼3单元1002 17800293735')

    class Meta:
        verbose_name = 'Manzil'
        verbose_name_plural = 'Manzillar'