from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, BooleanWidget, FloatWidget, DateWidget, IntegerWidget

from app.models import User, Referal, CreatedAt, Product


class UserResource(resources.ModelResource):
    full_name = Field(
        column_name='Полное имя',
        attribute='full_name',
    )
    phone_number = Field(
        column_name='Номер телефона',
        attribute='phone_number',
    )
    phone_number2 = Field(
        column_name='Номер телефона (доп)',
        attribute='phone_number2',
    )
    id_code = Field(
        column_name='ID код',
        attribute='id_code',
    )
    is_standart = Field(
        column_name='По стандарту',
        attribute='is_standart',
        widget=BooleanWidget()
    )
    is_kg = Field(
        column_name='По кг',
        attribute='is_kg',
        widget=BooleanWidget()
    )
    default_price = Field(
        column_name='Цена по умолчанию',
        attribute='default_price',
        widget=FloatWidget()
    )
    referal = Field(
        column_name='Реферал',
        attribute='referal',
        widget=ForeignKeyWidget(Referal, field='name')
    )

    class Meta:
        model = User
        fields = ('id', 'full_name', 'phone_number', 'phone_number2', 'id_code', 'is_standard', 'is_kg',
                  'default_price', 'referal')


class CreatedAtResource(resources.ModelResource):
    date = Field(
        column_name='Дата',
        attribute='date',
        widget=DateWidget(format="%d.%m.%Y")
    )
    consignment = Field(
        column_name='Партия',
        attribute='consignment',
    )
    expenses = Field(
        column_name='Расходы',
        attribute='expenses',
        widget=FloatWidget()
    )
    transport_expenses = Field(
        column_name='Транспортные расходы',
        attribute='transport_expenses',
        widget=FloatWidget()
    )
    tax = Field(
        column_name='Налоги',
        attribute='tax',
        widget=FloatWidget()
    )
    add_expenses = Field(
        column_name='Доп. расходы',
        attribute='add_expenses',
        widget=FloatWidget()
    )
    kg = Field(
        column_name='КГ',
        attribute='kg',
        widget=FloatWidget()
    )
    from_who = Field(
        column_name='От кого',
        attribute='from_who',
    )
    to_who = Field(
        column_name='К Кому',
        attribute='to_who',
    )

    class Meta:
        model = CreatedAt
        fields = (
            'id', 'date', 'consignment', 'expenses', 'transport_expenses', 'tax', 'add_expenses', 'kg', 'from_who',
            'to_who')


class ProductResource(resources.ModelResource):
    consignment = Field(
        column_name='Партия',
        attribute='consignment',
        widget=ForeignKeyWidget(model=CreatedAt, field='pk')
    )
    user = Field(
        column_name='Владелец',
        attribute='user',
        widget=ForeignKeyWidget(User, field="id_code")
    )
    trek_code = Field(
        column_name='Трек код',
        attribute='trek_code',
    )
    name = Field(
        column_name='Название',
        attribute='name',
    )
    quantity = Field(
        column_name='Количество',
        attribute='quantity',
        widget=IntegerWidget()
    )
    tall = Field(
        column_name='Длина',
        attribute='tall',
        widget=FloatWidget()
    )
    width = Field(
        column_name='Ширина',
        attribute='width',
        widget=FloatWidget()
    )
    height = Field(
        column_name='Высота',
        attribute='height',
        widget=FloatWidget()
    )
    standart_kg = Field(
        column_name='Стандарт вес',
        attribute='standart_kg',
        widget=FloatWidget()
    )
    own_kg = Field(
        column_name='Собственный вес',
        attribute='own_kg',
        widget=FloatWidget()
    )
    price = Field(
        column_name='Цена продукта',
        attribute='price',
        widget=FloatWidget()
    )
    service_price = Field(
        column_name='Цена услуги',
        attribute='service_price',
        widget=FloatWidget()
    )
    summary = Field(
        column_name='Суммарно',
        attribute='summary',
        widget=FloatWidget()
    )
    is_arrived = Field(
        column_name='Пришло в Узб?',
        attribute='is_arrived',
        widget=BooleanWidget()
    )
    is_taken = Field(
        column_name='Забрал клиент?',
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
    name = Field(column_name='Название', attribute='name')

    class Meta:
        model = Referal
        fields = ('id', 'name', 'quantity', 'link')
