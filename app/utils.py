import base64
import re
import unicodedata
from io import BytesIO

import qrcode
from barcode import Code128
from barcode.writer import ImageWriter
from django.conf import settings
from django.utils.functional import keep_lazy_text

from app.models import Product


def switch_lang_code(path, language):
    # Get the supported language codes
    lang_codes = [c for (c, name) in settings.LANGUAGES]

    # Validate the inputs
    if path == '':
        raise Exception('URL path for language switch is empty')
    elif path[0] != '/':
        raise Exception('URL path for language switch does not start with "/"')
    elif language not in lang_codes:
        raise Exception('%s is not a supported language code' % language)

    # Split the parts of the path
    parts = path.split('/')

    # Add or substitute the new language prefix
    if parts[1] in lang_codes:
        parts[1] = language
    else:
        parts[0] = "/" + language

    # Return the full new path
    return '/'.join(parts)


@keep_lazy_text
def custom_slugify(value, allow_unicode=True):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def get_next_in_date_hierarchy(request, date_hierarchy):
    if date_hierarchy + '__day' in request.GET:
        return 'hour'

    if date_hierarchy + '__month' in request.GET:
        return 'day'

    if date_hierarchy + '__year' in request.GET:
        return 'week'

    return 'month'


def product_or_products(product: Product):
    data = {
        "product_id": {
            "description": "Product ID",
            "value": product.id
        },
        "name": {
            "description": "Name",
            "value": product.name
        },
        "price": {
            "description": "Name",
            "value": product.price
        },
        "quantity": {
            "description": "Quantity",
            "value": product.quantity
        },
        "length": {
            "description": "Length",
            "value": product.tall
        },
        "width": {
            "description": "Width",
            "value": product.width
        },
        "height": {
            "description": "Height",
            "value": product.height
        },
        "weight": {
            "description": "Weight",
            "value": product.own_kg
        },
        "partiya": {
            "description": "Partiya",
            "value": product.consignment.batch_name
        },
        "dafou": {
            "description": "Dafou",
            "value": product.dafousi
        },
        "owner": {
            "description": "Owner",
            "value": product.user.phone_number
        },
        "trek_code": {
            "description": "Trek Code",
            "value": product.trek_code
        },
    }

    qr_data = '\n'.join([f"{i['description']}: {i['value']}" for i in data.values()])
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=1,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_buffered = BytesIO()
    qr_img.save(qr_buffered, format="PNG")
    qr_code_base64 = base64.b64encode(qr_buffered.getvalue()).decode('utf-8')

    barcode_writer = ImageWriter()
    barcode_writer.dpi = 1000
    barcode = Code128(str(product.id), writer=barcode_writer)
    barcode_buffered = BytesIO()
    barcode.write(barcode_buffered)
    barcode_base64 = base64.b64encode(barcode_buffered.getvalue()).decode('utf-8')
    context = {
        'product': product,
        'qr_code_base64': qr_code_base64,
        'data': data,
        'barcode_base64': barcode_base64,
    }

    return context
