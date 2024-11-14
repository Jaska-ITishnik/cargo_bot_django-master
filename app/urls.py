from django.urls import path

from app import views
from app.views import OwnerAutocomplete

app_name = "app"

urlpatterns = [
    path('is_taken/<int:product_id>', views.is_taken, name='is_taken'),
    path('is_arrived/<int:product_id>', views.is_arrived, name='is_arrived'),
    path('is_china/<int:product_id>', views.is_china, name='is_china'),

    path('not_is_taken/<int:product_id>', views.not_is_taken, name='not_is_taken'),
    path('not_is_arrived/<int:product_id>', views.not_is_arrived, name='not_is_arrived'),
    path('not_is_china/<int:product_id>', views.not_is_china, name='not_is_china'),

    path('owner-autocomplete/', OwnerAutocomplete.as_view(), name='owner-autocomplete'),
]
