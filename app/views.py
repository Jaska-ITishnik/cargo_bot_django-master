from dal import autocomplete
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from app.models import Product, User, Address
from utils import send_telegram_notification, taken_order, arrived, arrived_china


@csrf_exempt
def toggle_is_arrived(request, product_id):
    uzbek_address_uz = Address.objects.all().last().address_uzbek_uz
    uzbek_address_ru = Address.objects.all().last().address_uzbek_ru
    product = get_object_or_404(Product, id=product_id)
    if product.user and not product.is_arrived:
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
    product.is_arrived = not product.is_arrived
    product.save()
    return JsonResponse({
        'success': True,
        'product_id': product.id,
        'status_html': f"{'Yetib kelgan' if product.is_arrived else 'Yetib kelmagan'}"
    })


@csrf_exempt
def toggle_is_taken(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.user and not product.is_taken:
        if product.user.lang == 'uz':
            send_telegram_notification(taken_order[product.user.lang].format(product.trek_code), product.user.tg_id)
        else:
            send_telegram_notification(taken_order[product.user.lang].format(product.trek_code), product.user.tg_id)
    product.is_taken = not product.is_taken
    product.save()
    return JsonResponse({
        'success': True,
        'product_id': product.id,
        'status_html': f"{'Olib ketilgan' if product.is_taken else 'Olib ketilmagan'}"
    })


@csrf_exempt
def toggle_is_china(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.user and not product.is_china:
        send_telegram_notification(
            arrived_china[product.user.lang].format(product.trek_code, product.name, product.own_kg,
                                                    product.standart_kg),
            product.user.tg_id)
    product.is_china = not product.is_china
    product.save()
    return JsonResponse({
        'success': True,
        'product_id': product.id,
        'status_html': f"{'Xitoyda' if product.is_china else 'Xitoyda emas'}"
    })


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
