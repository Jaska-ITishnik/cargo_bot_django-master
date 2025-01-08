from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import Group
from django.urls import reverse
from import_export.admin import ImportExportActionModelAdmin

from app.forms import ProductForm
from app.models import User, Product, Comment, Referal, CreatedAt, Phones, ActivePhone, Address
from app.product_proxy import NotRegisteredProductProxy
from app.resources import UserResource, ReferalResource, ProductResource, CreatedAtResource


def get_app_list(self, request):
    app_dict = self._build_app_dict(request)

    app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
    for app in app_list:
        for model in app['models']:
            model_class = model['model']
            if model['object_name'] == 'Product':
                model['count'] = Product.objects.filter(user__isnull=False).count()
            else:
                model['count'] = model_class.objects.count()
    return app_list


from django.utils.safestring import mark_safe

admin.AdminSite.get_app_list = get_app_list


@admin.register(User)
class UserAdmin(ImportExportActionModelAdmin):
    list_display = [
        'id_code', 'full_name', 'phone_number', 'qoshimcha_tel', 'summary',
        'oldi_passport', 'orqa_passport', 'rasmi', 'referal'
    ]
    resource_class = UserResource
    search_fields = 'id_code', 'full_name', 'phone_number', 'phone_number2'
    list_filter = 'id_code', 'full_name', 'phone_number', 'phone_number2', 'referal'
    exclude = "latitude", "longitude", "is_active", "tg_id", 'referal', 'lang'

    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',)
        }

    def summary(self, obj):
        r = obj.products.all().values_list('is_taken', 'summary')
        if len(r) >= 1 and not r[0][0]:
            return r[0][1]
        return 0

    summary.short_description = 'Umumiy summa'

    def qoshimcha_tel(self, obj):
        if obj.phone_number2:
            return obj.phone_number2
        else:
            return '-'

    qoshimcha_tel.short_description = "Qo'shimcha telefon"

    def oldi_passport(self, obj):
        if obj.passport1:
            return mark_safe(
                f'<a href="{obj.passport1.url}"><img src="{obj.passport1.url}" width="70px" height="70px"></a>')
        else:
            return "Rasmi yo'q"

    oldi_passport.short_description = "Pasport old tomoni"

    def orqa_passport(self, obj):
        if obj.passport2:
            return mark_safe(
                f'<a href="{obj.passport2.url}"><img src="{obj.passport2.url}" width="70px" height="70px"></a>')
        else:
            return "Rasm yo'q"

    orqa_passport.short_description = "Pasport orqa tomoni"

    def rasmi(self, obj):
        if obj.image:
            return mark_safe(f'<a href="{obj.image.url}"><img src="{obj.image.url}" width="70px" height="70px"></a>')
        else:
            return "Rasmi yo'q"

    def __str__(self):
        return f"{self.full_name} ({self.id_code})" if self.full_name and self.id_code else "Unnamed User"

    rasmi.short_description = "Rasmi"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment')


@admin.register(Referal)
class ReferalAdmin(ImportExportActionModelAdmin):
    list_display = ('name', 'link', 'quantity', 'total_products', 'total_summary')
    resource_class = ReferalResource
    search_fields = ('name',)
    list_filter = ('name', 'quantity')
    exclude = ('link', 'quantity')

    def total_products(self, obj):
        return Product.objects.filter(user__referal=obj).count()

    total_products.short_description = "Jami tovarlar"

    def total_summary(self, obj):
        r = Product.objects.filter(user__referal=obj).values_list('summary', flat=True)
        if len(r) >= 1:
            return r

    total_summary.short_description = "Umumiy summa"


@admin.register(Product)
class ProductAdmin(ImportExportActionModelAdmin):
    list_display = (
        'user_id_code', 'unregistered_user_phone', 'trek_code', 'name', 'quantity', 'tall', 'width', 'height',
        'standart_kg',
        'own_kg', 'dafousi', 'Xizmat_narxi', 'daofu_calculation', 'user_full_name', 'phone_number', 'status',
        'change_status_buttons', 'photo')
    list_display_links = ('user_id_code', 'trek_code', 'name')
    resource_class = ProductResource
    search_fields = (
        'user', 'name', 'tall', 'width', 'height', 'standart_kg',
        'own_kg', 'daofu',
        'summary', 'is_arrived')
    list_filter = (
        'user', 'name', 'tall', 'width', 'height', 'standart_kg',
        'own_kg', 'daofu',
        'summary', 'is_arrived', 'is_taken', 'consignment')
    exclude = 'summary',
    form = ProductForm

    class Media:
        js = 'app/js/without_refresh.js',

    def get_queryset(self, request):
        return super().get_queryset(request).filter(user__isnull=False)

    def status(self, obj):
        res = ""
        if obj.is_arrived and not obj.is_taken:
            res = """<svg width="27" height="27" viewBox="0 0 31 31" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path fill-rule="evenodd" clip-rule="evenodd" d="M15.5 31C24.0604 31 31 24.0604 31 15.5C31 6.93959 24.0604 0 15.5 0C6.93959 0 0 6.93959 0 15.5C0 24.0604 6.93959 31 15.5 31ZM23.7795 10.1264C24.1255 9.69588 24.0569 9.06644 23.6264 8.72049C23.1959 8.37455 22.5664 8.4431 22.2205 8.87361L13.2082 20.0889L8.63155 16.361C8.20334 16.0122 7.57346 16.0766 7.22466 16.5048C6.87587 16.933 6.94025 17.5629 7.36845 17.9117L11.9451 21.6396C12.8055 22.3405 14.0721 22.2068 14.7672 21.3417L23.7795 10.1264Z" fill="#71BF2A"/>
    </svg>"""
        elif obj.is_arrived and obj.is_taken:
            res = """<svg width="27" height="27" viewBox="0 0 32 31" fill="none" xmlns="http://www.w3.org/2000/svg">
<path fill-rule="evenodd" clip-rule="evenodd" d="M31.5 15.5C31.5 24.0604 24.5604 31 16 31C7.43959 31 0.5 24.0604 0.5 15.5C0.5 6.93959 7.43959 0 16 0C24.5604 0 31.5 6.93959 31.5 15.5ZM25.6334 9.22604C26.0608 9.57577 26.1238 10.2058 25.7741 10.6332L17.4004 20.8677C16.7064 21.716 15.4589 21.8477 14.6031 21.163L12.5213 19.4976L11.381 20.8913C10.7023 21.7208 9.49047 21.8679 8.63309 21.2248L5.4 18.8C4.95817 18.4686 4.86863 17.8418 5.2 17.4C5.53137 16.9582 6.15817 16.8686 6.6 17.2L9.83309 19.6248L10.9595 18.2481L10.3754 17.7809C9.94417 17.4359 9.87424 16.8066 10.2193 16.3753C10.5643 15.944 11.1936 15.8741 11.6248 16.2191L12.226 16.7001L18.226 9.36677C18.5758 8.93932 19.2058 8.87632 19.6332 9.22605C20.0607 9.57577 20.1237 10.2058 19.774 10.6332L13.7879 17.9496L15.8525 19.6013L24.2262 9.36676C24.5759 8.93932 25.2059 8.87632 25.6334 9.22604Z" fill="#71BF2A"/>
</svg>
"""
        elif obj.is_china:
            res = """<svg width="30" height="30" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 2C6.49 2 2 6.49 2 12C2 17.51 6.49 22 12 22C17.51 22 22 17.51 22 12C22 6.49 17.51 2 12 2ZM16.35 15.57C16.21 15.81 15.96 15.94 15.7 15.94C15.57 15.94 15.44 15.91 15.32 15.83L12.22 13.98C11.45 13.52 10.88 12.51 10.88 11.62V7.52C10.88 7.11 11.22 6.77 11.63 6.77C12.04 6.77 12.38 7.11 12.38 7.52V11.62C12.38 11.98 12.68 12.51 12.99 12.69L16.09 14.54C16.45 14.75 16.57 15.21 16.35 15.57Z" fill="#ffa900"/>
</svg>"""
        else:
            res = """<svg width="27" height="27" viewBox="0 0 31 31" fill="none" xmlns="http://www.w3.org/2000/svg">
<path fill-rule="evenodd" clip-rule="evenodd" d="M31 15.5C31 24.0604 24.0604 31 15.5 31C6.93959 31 0 24.0604 0 15.5C0 6.93959 6.93959 0 15.5 0C24.0604 0 31 6.93959 31 15.5ZM22.2071 8.79289C22.5976 9.18342 22.5976 9.81658 22.2071 10.2071L16.9142 15.5L22.2071 20.7929C22.5976 21.1834 22.5976 21.8166 22.2071 22.2071C21.8166 22.5976 21.1834 22.5976 20.7929 22.2071L15.5 16.9142L10.2071 22.2071C9.81658 22.5976 9.18342 22.5976 8.79289 22.2071C8.40237 21.8166 8.40237 21.1834 8.79289 20.7929L14.0858 15.5L8.79289 10.2071C8.40237 9.81658 8.40237 9.18342 8.79289 8.79289C9.18342 8.40237 9.81658 8.40237 10.2071 8.79289L15.5 14.0858L20.7929 8.79289C21.1834 8.40237 21.8166 8.40237 22.2071 8.79289Z" fill="#FF0000"/>
</svg>
"""
        return mark_safe(res)

    def change_status_buttons(self, obj):
        return mark_safe(f"""
            <div id="status-{obj.id}">
                <a href="#" 
                    class="status-change-button"
                    style="display: inline-block; margin-top: 10px; width: 100px; padding: 10px 10px; text-align: center; text-decoration: none; color: #fff; background-color: {'#007bff' if obj.is_arrived else 'red'}; border: 1px solid #ffc107; border-radius: 5px; font-size: 14px; transition: background-color 0.3s ease, color 0.3s ease;"
                    data-url="{reverse('app:toggle_is_arrived', args=[obj.id])}">{'Yetib kelgan' if obj.is_arrived else 'Yetib kelmagan'}
                </a>
                <a href="#"  
                    class="status-change-button"
                    style="display: inline-block; margin-top: 10px; width: 100px; padding: 10px  10px; text-align: center; text-decoration: none; color: #fff; background-color: {'#007bff' if obj.is_taken else 'red'}; border: 1px solid #ffc107; border-radius: 5px; font-size: 14px; transition: background-color 0.3s ease, color 0.3s ease;"
                    data-url="{reverse('app:toggle_is_taken', args=[obj.id])}">{'Olib ketgan' if obj.is_taken else 'Olib ketmagan'}</a>
                <a href="#"  
                    class="status-change-button"
                    style="display: inline-block; margin-top: 10px; width: 100px; padding: 10px  10px; text-align: center; text-decoration: none; color: #fff; background-color: {'#007bff' if obj.is_china else 'red'}; border: 1px solid #ffc107; border-radius: 5px; font-size: 14px; transition: background-color 0.3s ease, color 0.3s ease;"
                    data-url="{reverse('app:toggle_is_china', args=[obj.id])}">{'Xitoyda' if obj.is_china else 'Xitoyda emas'}</a>
            </div>
        """)

    change_status_buttons.short_description = "Holatini o'zgartirish"

    def user_id_code(self, obj):
        if obj.user:
            return obj.user.id_code
        return "ro'yxatdan o'tilmagan -> "

    user_id_code.short_description = 'Egasining ID kodi'

    def user_full_name(self, obj):
        if obj.user:
            return obj.user.full_name
        return "-"

    user_full_name.short_description = "Egasining to'liq ismi"

    def phone_number(self, obj):
        if obj.user:
            return obj.user.phone_number
        return '-'

    phone_number.short_description = "Egasining telefon raqami"

    def photo(self, obj):
        if obj.image:
            return mark_safe(f'<a href="{obj.image.url}"><img src="{obj.image.url}" width="70px" height="70px"></a>')
        else:
            return "Rasmi yo'q"

    photo.short_description = 'Mahsulot fotosurati'

    @admin.display(description='Jami')
    def daofu_calculation(self, obj: Product):
        if obj.daofu:
            return f"💲{round(obj.own_kg * obj.service_price + obj.daofu / obj.consignment.yuan_dollar, 2)}"
        return f"💲{round(obj.own_kg * obj.service_price, 2)}"


@admin.register(NotRegisteredProductProxy)
class NotRegisteredProductProxyModelAdmin(ImportExportActionModelAdmin):
    list_display = (
        'unregistered_user_phone', 'trek_code', 'name', 'quantity', 'tall', 'width', 'height',
        'standart_kg',
        'own_kg', 'daofu', 'service_price', 'daofu_calculation', 'user_full_name', 'status', 'change_status_buttons'
    )
    resource_class = ProductResource

    class Media:
        js = 'app/js/without_refresh.js',

    @admin.display(description='Jami')
    def daofu_calculation(self, obj: Product):
        if obj.daofu:
            return round(obj.own_kg * obj.service_price + obj.daofu / obj.consignment.yuan_dollar, 2)
        return round(obj.own_kg * obj.service_price, 2)

    def user_full_name(self, obj):
        if obj.user:
            return obj.user.full_name
        return "-"

    def status(self, obj):
        res = ""
        if obj.is_arrived and not obj.is_taken:
            res = """<svg width="27" height="27" viewBox="0 0 31 31" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path fill-rule="evenodd" clip-rule="evenodd" d="M15.5 31C24.0604 31 31 24.0604 31 15.5C31 6.93959 24.0604 0 15.5 0C6.93959 0 0 6.93959 0 15.5C0 24.0604 6.93959 31 15.5 31ZM23.7795 10.1264C24.1255 9.69588 24.0569 9.06644 23.6264 8.72049C23.1959 8.37455 22.5664 8.4431 22.2205 8.87361L13.2082 20.0889L8.63155 16.361C8.20334 16.0122 7.57346 16.0766 7.22466 16.5048C6.87587 16.933 6.94025 17.5629 7.36845 17.9117L11.9451 21.6396C12.8055 22.3405 14.0721 22.2068 14.7672 21.3417L23.7795 10.1264Z" fill="#71BF2A"/>
        </svg>"""
        elif obj.is_arrived and obj.is_taken:
            res = """<svg width="27" height="27" viewBox="0 0 32 31" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path fill-rule="evenodd" clip-rule="evenodd" d="M31.5 15.5C31.5 24.0604 24.5604 31 16 31C7.43959 31 0.5 24.0604 0.5 15.5C0.5 6.93959 7.43959 0 16 0C24.5604 0 31.5 6.93959 31.5 15.5ZM25.6334 9.22604C26.0608 9.57577 26.1238 10.2058 25.7741 10.6332L17.4004 20.8677C16.7064 21.716 15.4589 21.8477 14.6031 21.163L12.5213 19.4976L11.381 20.8913C10.7023 21.7208 9.49047 21.8679 8.63309 21.2248L5.4 18.8C4.95817 18.4686 4.86863 17.8418 5.2 17.4C5.53137 16.9582 6.15817 16.8686 6.6 17.2L9.83309 19.6248L10.9595 18.2481L10.3754 17.7809C9.94417 17.4359 9.87424 16.8066 10.2193 16.3753C10.5643 15.944 11.1936 15.8741 11.6248 16.2191L12.226 16.7001L18.226 9.36677C18.5758 8.93932 19.2058 8.87632 19.6332 9.22605C20.0607 9.57577 20.1237 10.2058 19.774 10.6332L13.7879 17.9496L15.8525 19.6013L24.2262 9.36676C24.5759 8.93932 25.2059 8.87632 25.6334 9.22604Z" fill="#71BF2A"/>
    </svg>
    """
        elif obj.is_china:
            res = """<svg width="30" height="30" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2C6.49 2 2 6.49 2 12C2 17.51 6.49 22 12 22C17.51 22 22 17.51 22 12C22 6.49 17.51 2 12 2ZM16.35 15.57C16.21 15.81 15.96 15.94 15.7 15.94C15.57 15.94 15.44 15.91 15.32 15.83L12.22 13.98C11.45 13.52 10.88 12.51 10.88 11.62V7.52C10.88 7.11 11.22 6.77 11.63 6.77C12.04 6.77 12.38 7.11 12.38 7.52V11.62C12.38 11.98 12.68 12.51 12.99 12.69L16.09 14.54C16.45 14.75 16.57 15.21 16.35 15.57Z" fill="#ffa900"/>
    </svg>"""
        else:
            res = """<svg width="27" height="27" viewBox="0 0 31 31" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path fill-rule="evenodd" clip-rule="evenodd" d="M31 15.5C31 24.0604 24.0604 31 15.5 31C6.93959 31 0 24.0604 0 15.5C0 6.93959 6.93959 0 15.5 0C24.0604 0 31 6.93959 31 15.5ZM22.2071 8.79289C22.5976 9.18342 22.5976 9.81658 22.2071 10.2071L16.9142 15.5L22.2071 20.7929C22.5976 21.1834 22.5976 21.8166 22.2071 22.2071C21.8166 22.5976 21.1834 22.5976 20.7929 22.2071L15.5 16.9142L10.2071 22.2071C9.81658 22.5976 9.18342 22.5976 8.79289 22.2071C8.40237 21.8166 8.40237 21.1834 8.79289 20.7929L14.0858 15.5L8.79289 10.2071C8.40237 9.81658 8.40237 9.18342 8.79289 8.79289C9.18342 8.40237 9.81658 8.40237 10.2071 8.79289L15.5 14.0858L20.7929 8.79289C21.1834 8.40237 21.8166 8.40237 22.2071 8.79289Z" fill="#FF0000"/>
    </svg>
    """
        return mark_safe(res)

    def change_status_buttons(self, obj):
        return mark_safe(f"""
            <div id="status-{obj.id}">
                <a href="#" 
                    class="status-change-button"
                    style="display: inline-block; margin-top: 10px; width: 100px; padding: 10px 10px; text-align: center; text-decoration: none; color: #fff; background-color: {'#007bff' if obj.is_arrived else 'red'}; border: 1px solid #ffc107; border-radius: 5px; font-size: 14px; transition: background-color 0.3s ease, color 0.3s ease;"
                    data-url="{reverse('app:toggle_is_arrived', args=[obj.id])}">{'Yetib kelgan' if obj.is_arrived else 'Yetib kelmagan'}
                </a>
                <a href="#"  
                    class="status-change-button"
                    style="display: inline-block; margin-top: 10px; width: 100px; padding: 10px  10px; text-align: center; text-decoration: none; color: #fff; background-color: {'#007bff' if obj.is_taken else 'red'}; border: 1px solid #ffc107; border-radius: 5px; font-size: 14px; transition: background-color 0.3s ease, color 0.3s ease;"
                    data-url="{reverse('app:toggle_is_taken', args=[obj.id])}">{'Olib ketgan' if obj.is_taken else 'Olib ketmagan'}</a>
                <a href="#"  
                    class="status-change-button"
                    style="display: inline-block; margin-top: 10px; width: 100px; padding: 10px  10px; text-align: center; text-decoration: none; color: #fff; background-color: {'#007bff' if obj.is_china else 'red'}; border: 1px solid #ffc107; border-radius: 5px; font-size: 14px; transition: background-color 0.3s ease, color 0.3s ease;"
                    data-url="{reverse('app:toggle_is_china', args=[obj.id])}">{'Xitoyda' if obj.is_china else 'Xitoyda emas'}</a>
            </div>
        """)

    change_status_buttons.short_description = "Holatini o'zgartirish"


@admin.register(CreatedAt)
class CreatedAtAdmin(ImportExportActionModelAdmin):
    list_display = [
        'id', 'date', 'consignment', 'expenses', 'transport_expenses',
        'tax', 'add_expenses', 'summary_weight', 'kg', 'general_sum',
        'general_expenses', 'general_profit', 'kg1', 'from_who',
        'to_who', 'yuan_dollar', 'dollar_sum'
    ]
    list_filter = 'date', 'consignment'
    resource_class = CreatedAtResource

    @admin.display(description="Umumiy og'irlik")
    def summary_weight(self, obj: CreatedAt):
        r = Product.objects.filter(consignment=obj).values_list('own_kg', flat=True)
        if len(r) >= 1:
            return sum(r)
        return 0

    @admin.display(description="Jami")
    def general_sum(self, obj: CreatedAt):
        products = Product.objects.filter(consignment=obj)
        all_amount = []
        for product in products:
            all_amount.append(
                round(product.own_kg * product.service_price + product.daofu / product.consignment.yuan_dollar, 2))
        return sum(all_amount)

    def general_expenses(self, obj):
        if obj.expenses and obj.transport_expenses and obj.tax and obj.add_expenses:
            return obj.expenses + obj.transport_expenses + obj.tax + obj.add_expenses
        return 'Aniq emas'

    general_expenses.short_description = 'Umumiy xarajatlar'

    def general_profit(self, obj):
        r = obj.products.all().values_list('summary', flat=True)
        summary = 0
        expenses = 0
        if len(r) >= 1:
            summary = sum(r)
        if obj.expenses and obj.transport_expenses and obj.tax and obj.add_expenses:
            expenses = obj.expenses + obj.transport_expenses + obj.tax + obj.add_expenses
        return summary - expenses

    general_profit.short_description = 'Umumiy xarajatlar'

    def kg1(self, obj):
        if obj.expenses is not None and obj.transport_expenses is not None and obj.tax is not None and obj.add_expenses is not None:
            res = obj.expenses + obj.transport_expenses + obj.tax + obj.add_expenses
            return res / obj.kg
        return "Aniq emas"

    kg1.short_description = '1 kg uchun'


@admin.register(Address)
class AddressModelAdmin(ModelAdmin):
    list_display = 'period_avia', 'period_avto', 'phone_number', 'mail_address', 'address', 'address_uzbek_uz', 'address_uzbek_ru'


admin.site.register(Phones)
admin.site.register(ActivePhone)
admin.site.unregister(Group)
