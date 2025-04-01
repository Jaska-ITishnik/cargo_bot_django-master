from app.views import OwnerAutocomplete, toggle_is_arrived, toggle_is_taken, toggle_is_china, not_is_taken, \
    not_is_arrived, not_is_china, product_detail_qrcode, product_detail_qrcode_cons

app_name = "app"
from django.urls import path

urlpatterns = [
    # path('is_taken/<int:product_id>', views.is_taken, name='is_taken'),
    # path('is_arrived/<int:product_id>', views.is_arrived, name='is_arrived'),
    # path('is_china/<int:product_id>', views.is_china, name='is_china'),
    path('print-product-consignment/<int:consignment_id>/', product_detail_qrcode_cons, name='print_product_consignment'),
    path('print-product/<int:product_id>/', product_detail_qrcode, name='print_product'),
    path('toggle-is-arrived/<int:product_id>/', toggle_is_arrived, name='toggle_is_arrived'),
    path('toggle-is-taken/<int:product_id>/', toggle_is_taken, name='toggle_is_taken'),
    path('toggle-is-china/<int:product_id>/', toggle_is_china, name='toggle_is_china'),

    path('not_is_taken/<int:product_id>', not_is_taken, name='not_is_taken'),
    path('not_is_arrived/<int:product_id>', not_is_arrived, name='not_is_arrived'),
    path('not_is_china/<int:product_id>', not_is_china, name='not_is_china'),
    path('owner-autocomplete/', OwnerAutocomplete.as_view(), name='owner-autocomplete'),
]
