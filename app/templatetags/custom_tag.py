from django.template import Library

register = Library()


@register.filter()
def calculation_amount(obj):
    if obj:
        pass

