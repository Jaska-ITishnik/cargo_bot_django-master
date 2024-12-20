from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, BooleanWidget, FloatWidget, DateWidget, IntegerWidget

from app.models import User, Referal, CreatedAt, Product


class UserResource(resources.ModelResource):
    full_name = Field(
        column_name="To'liq ismi",
        attribute='full_name',
    )
    phone_number = Field(
        column_name='Telefon nomeri',
        attribute='phone_number',
    )
    phone_number2 = Field(
        column_name="Telefon nomeri (qo'sh)",
        attribute='phone_number2',
    )
    id_code = Field(
        column_name='ID kod',
        attribute='id_code',
    )
    is_standart = Field(
        column_name='Standartmi',
        attribute='is_standart',
        widget=BooleanWidget()
    )
    is_kg = Field(
        column_name='Kg mi',
        attribute='is_kg',
        widget=BooleanWidget()
    )
    default_price = Field(
        column_name='Standart narx',
        attribute='default_price',
        widget=FloatWidget()
    )
    referal = Field(
        column_name='Refferal',
        attribute='referal',
        widget=ForeignKeyWidget(Referal, field='name')
    )

    class Meta:
        model = User
        fields = ('id', 'full_name', 'phone_number', 'phone_number2', 'id_code', 'is_standard', 'is_kg',
                  'default_price', 'referal')


class CreatedAtResource(resources.ModelResource):
    date = Field(
        column_name='Sana',
        attribute='date',
        widget=DateWidget(format="%d.%m.%Y")
    )
    consignment = Field(
        column_name='Partiya',
        attribute='consignment',
    )
    expenses = Field(
        column_name='Xarajatlar',
        attribute='expenses',
        widget=FloatWidget()
    )
    transport_expenses = Field(
        column_name='Transport xarajatlari',
        attribute='transport_expenses',
        widget=FloatWidget()
    )
    tax = Field(
        column_name='Soqlilar',
        attribute='tax',
        widget=FloatWidget()
    )
    add_expenses = Field(
        column_name="Qo'shimcha. xarajatlar",
        attribute='add_expenses',
        widget=FloatWidget()
    )
    kg = Field(
        column_name='Kg',
        attribute='kg',
        widget=FloatWidget()
    )
    from_who = Field(
        column_name='Kim tomonidan',
        attribute='from_who',
    )
    to_who = Field(
        column_name='Kimga',
        attribute='to_who',
    )

    class Meta:
        model = CreatedAt
        fields = (
            'id', 'date', 'consignment', 'expenses', 'transport_expenses', 'tax', 'add_expenses', 'kg', 'from_who',
            'to_who')


class ProductResource(resources.ModelResource):
    consignment = Field(
        column_name='Partiya',
        attribute='consignment',
        widget=ForeignKeyWidget(model=CreatedAt, field='pk')
    )
    user = Field(
        column_name='Egasi',
        attribute='user',
        widget=ForeignKeyWidget(User, field="id_code")
    )

    unregistered_user_phone = Field(
        column_name="Ro'yxatdan o'tmagan userni telefoni",
        attribute='unregistered_user_phone',
    )

    trek_code = Field(
        column_name='Trek kodi',
        attribute='trek_code',
    )
    name = Field(
        column_name='Nomi',
        attribute='name',
    )
    quantity = Field(
        column_name='Soni',
        attribute='quantity',
        widget=IntegerWidget()
    )
    tall = Field(
        column_name='Uzunligi',
        attribute='tall',
        widget=FloatWidget()
    )
    width = Field(
        column_name='Kengligi',
        attribute='width',
        widget=FloatWidget()
    )
    height = Field(
        column_name='Balandligi',
        attribute='height',
        widget=FloatWidget()
    )
    standart_kg = Field(
        column_name="Standart og'irligi",
        attribute='standart_kg',
        widget=FloatWidget()
    )
    own_kg = Field(
        column_name='Sof vazni',
        attribute='own_kg',
        widget=FloatWidget()
    )
    price = Field(
        column_name='Maxsulot narxi',
        attribute='price',
        widget=FloatWidget()
    )
    service_price = Field(
        column_name='Xizmat narxi',
        attribute='service_price',
        widget=FloatWidget()
    )
    summary = Field(
        column_name='Jami',
        attribute='summary',
        widget=FloatWidget()
    )
    is_china = Field(
        column_name='Uzb ga keldimi?',
        attribute='is_arrived',
        widget=BooleanWidget()
    )
    is_arrived = Field(
        column_name='Xitoyda emasmi?',
        attribute='is_arrived',
        widget=BooleanWidget()
    )
    is_taken = Field(
        column_name='Klient olib kettimi?',
        attribute='is_taken',
        widget=BooleanWidget()
    )
    daofu = Field(
        column_name='Daofu',
        attribute='daofu',
        widget=FloatWidget()
    )

    class Meta:
        model = Product
        fields = (
            'id', 'consignment', 'user', 'trek_code', 'name', 'quantity', 'tall', 'width', 'height', 'standart_kg',
            'own_kg', 'price', 'service_price', 'summary', 'is_arrived', 'is_taken', 'daofu')


class ReferalResource(resources.ModelResource):
    name = Field(column_name='Nomi', attribute='name')

    class Meta:
        model = Referal
        fields = ('id', 'name', 'quantity', 'link')
