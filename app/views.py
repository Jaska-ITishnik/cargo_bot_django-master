from dal import autocomplete
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView

from app.models import Address, ActivePhone, Comment, CreatedAt, Referal, Phones
from app.models import Product, User
from app.product_proxy import NotRegisteredProductProxy
from utils import send_telegram_notification, arrived, arrived_china, taken_order


def is_taken(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product.user:
        if product.user.lang == 'uz':
            send_telegram_notification(taken_order[product.user.lang].format(product.trek_code), product.user.tg_id)
        else:
            send_telegram_notification(taken_order[product.user.lang].format(product.trek_code), product.user.tg_id)
    product.is_taken = True
    product.save()
    return redirect(reverse('admin:app_product_changelist'))


def is_arrived(request, product_id):
    uzbek_address_uz = Address.objects.all().last().address_uzbek_uz
    uzbek_address_ru = Address.objects.all().last().address_uzbek_ru
    product = get_object_or_404(Product, pk=product_id)
    if product.user:
        if product.user.lang == 'uz':
            if product.image:
                send_telegram_notification(
                    arrived[product.user.lang].format(product.trek_code, product.name, product.own_kg,
                                                      product.standart_kg,
                                                      product.summary, product.dafousi, uzbek_address_uz),
                    product.user.tg_id, product.image.path)
            else:
                send_telegram_notification(
                    arrived[product.user.lang].format(product.trek_code, product.name, product.own_kg,
                                                      product.standart_kg,
                                                      product.summary, product.dafousi, uzbek_address_uz),
                    product.user.tg_id)
        else:
            if product.image:
                send_telegram_notification(
                    arrived[product.user.lang].format(product.trek_code, product.name, product.own_kg,
                                                      product.standart_kg,
                                                      product.summary, product.dafousi, uzbek_address_ru),
                    product.user.tg_id, product.image.path)
            else:
                send_telegram_notification(
                    arrived[product.user.lang].format(product.trek_code, product.name, product.own_kg,
                                                      product.standart_kg,
                                                      product.summary, product.dafousi, uzbek_address_ru),
                    product.user.tg_id)
    product.is_arrived = True
    product.save()
    if product.user:
        return redirect(reverse('admin:app_product_changelist'))
    return redirect(reverse('admin:app_notregisteredproductproxy_changelist'))


def is_china(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product.user:
        send_telegram_notification(
            arrived_china[product.user.lang].format(product.trek_code, product.name, product.own_kg,
                                                    product.standart_kg),
            product.user.tg_id)
    product.is_china = True
    product.save()
    if product.user:
        return redirect(reverse('admin:app_product_changelist'))
    return redirect(reverse('admin:app_notregisteredproductproxy_changelist'))


def not_is_taken(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.is_taken = False
    product.save()
    if product.user:
        return redirect(reverse('admin:app_product_changelist'))
    return redirect(reverse('admin:app_notregisteredproductproxy_changelist'))


def not_is_arrived(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.is_arrived = False
    product.save()
    if product.user:
        return redirect(reverse('admin:app_product_changelist'))
    return redirect(reverse('admin:app_notregisteredproductproxy_changelist'))


def not_is_china(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.is_china = False
    product.save()
    if product.user:
        return redirect(reverse('admin:app_product_changelist'))
    return redirect(reverse('admin:app_notregisteredproductproxy_changelist'))


class OwnerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return User.objects.none()

        qs = User.objects.all()

        if self.q:
            qs = qs.filter(id_code__icontains=self.q)

        return qs

