from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, BooleanWidget, FloatWidget, DateWidget, IntegerWidget
from django.utils.translation import gettext_lazy as _

from app.models import User, Referal, CreatedAt, Product


class UserResource(resources.ModelResource):
    full_name = Field(
        column_name=_("To'liq ismi"),
        attribute='full_name',
    )
    phone_number = Field(
        column_name=_('Telefon nomeri'),
        attribute='phone_number',
    )
    phone_number2 = Field(
        column_name=_("Telefon nomeri (qo'sh)"),
        attribute='phone_number2',
    )
    id_code = Field(
        column_name=_('ID kod'),
        attribute='id_code',
    )
    is_standart = Field(
        column_name=_('Standartmi'),
        attribute='is_standart',
        widget=BooleanWidget()
    )
    is_kg = Field(
        column_name=_('Kg mi'),
        attribute='is_kg',
        widget=BooleanWidget()
    )
    default_price = Field(
        column_name=_('Standart narx'),
        attribute='default_price',
        widget=FloatWidget()
    )
    referal = Field(
        column_name=_('Refferal'),
        attribute='referal',
        widget=ForeignKeyWidget(Referal, field='name')
    )

    class Meta:
        model = User
        fields = ('id', 'full_name', 'phone_number', 'phone_number2', 'id_code', 'is_standard', 'is_kg',
                  'default_price', 'referal')


class CreatedAtResource(resources.ModelResource):
    date = Field(
        column_name=_('Sana'),
        attribute='date',
        widget=DateWidget(format="%d.%m.%Y")
    )
    consignment = Field(
        column_name=_('Partiya'),
        attribute='consignment',
    )
    expenses = Field(
        column_name=_('Xarajatlar'),
        attribute='expenses',
        widget=FloatWidget()
    )
    transport_expenses = Field(
        column_name=_('Transport xarajatlari'),
        attribute='transport_expenses',
        widget=FloatWidget()
    )
    tax = Field(
        column_name=_('Soqlilar'),
        attribute='tax',
        widget=FloatWidget()
    )
    add_expenses = Field(
        column_name=_("Qo'shimcha. xarajatlar"),
        attribute='add_expenses',
        widget=FloatWidget()
    )
    kg = Field(
        column_name=_('Kg'),
        attribute='kg',
        widget=FloatWidget()
    )
    from_who = Field(
        column_name=_('Kim tomonidan'),
        attribute='from_who',
    )
    to_who = Field(
        column_name=_('Kimga'),
        attribute='to_who',
    )

    class Meta:
        model = CreatedAt
        fields = (
            'id', 'date', 'consignment', 'expenses', 'transport_expenses', 'tax', 'add_expenses', 'kg', 'from_who',
            'to_who')


class ProductResource(resources.ModelResource):
    consignment = Field(
        column_name=_('Partiya'),
        attribute='consignment',
        widget=ForeignKeyWidget(model=CreatedAt, field='pk')
    )
    user = Field(
        column_name=_('Egasi'),
        attribute='user',
        widget=ForeignKeyWidget(User, field="id_code")
    )

    unregistered_user_phone = Field(
        column_name=_("Ro'yxatdan o'tmagan userni telefoni"),
        attribute='unregistered_user_phone',
    )

    trek_code = Field(
        column_name=_('Trek kodi'),
        attribute='trek_code',
    )
    name = Field(
        column_name=_('Nomi'),
        attribute='name',
    )
    quantity = Field(
        column_name=_('Soni'),
        attribute='quantity',
        widget=IntegerWidget()
    )
    tall = Field(
        column_name=_('Uzunligi'),
        attribute='tall',
        widget=FloatWidget()
    )
    width = Field(
        column_name=_('Kengligi'),
        attribute='width',
        widget=FloatWidget()
    )
    height = Field(
        column_name=_('Balandligi'),
        attribute='height',
        widget=FloatWidget()
    )
    standart_kg = Field(
        column_name=_("Standart og'irligi"),
        attribute='standart_kg',
        widget=FloatWidget()
    )
    own_kg = Field(
        column_name=_('Sof vazni'),
        attribute='own_kg',
        widget=FloatWidget()
    )
    price = Field(
        column_name=_('Maxsulot narxi'),
        attribute='price',
        widget=FloatWidget()
    )
    service_price = Field(
        column_name=_('Xizmat narxi'),
        attribute='service_price',
        widget=FloatWidget()
    )
    summary = Field(
        column_name=_('Jami'),
        attribute='summary',
        widget=FloatWidget()
    )
    is_china = Field(
        column_name=_('Uzb ga keldimi?'),
        attribute='is_arrived',
        widget=BooleanWidget()
    )
    is_arrived = Field(
        column_name=_('Xitoyda emasmi?'),
        attribute='is_arrived',
        widget=BooleanWidget()
    )
    is_taken = Field(
        column_name=_('Klient olib kettimi?'),
        attribute='is_taken',
        widget=BooleanWidget()
    )
    daofu = Field(
        column_name=_('Daofu'),
        attribute='daofu',
        widget=FloatWidget()
    )

    class Meta:
        model = Product
        fields = (
            'id', 'consignment', 'user', 'trek_code', 'name', 'quantity', 'tall', 'width', 'height', 'standart_kg',
            'own_kg', 'price', 'service_price', 'summary', 'is_arrived', 'is_taken', 'daofu')

    def before_import_row(self, row, **kwargs):
        """Skip rows where critical fields are missing to prevent errors"""
        critical_fields = ['own_kg', 'service_price']

        # Check if any critical field is missing
        if any(row.get(field) in [None, ""] for field in critical_fields):
            return None  # Skip this row

        return super().before_import_row(row, **kwargs)


class ReferalResource(resources.ModelResource):
    name = Field(column_name=_('Nomi'), attribute='name')

    class Meta:
        model = Referal
        fields = ('id', 'name', 'quantity', 'link')
