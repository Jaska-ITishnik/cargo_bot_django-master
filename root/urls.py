from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from root import settings

title = _("❄️ Fad Cargo Administration ❄️")
admin.site.site_header = mark_safe(
    f"""
    <div style='display: flex; align-items: center; gap: 10px;'>
        <img style='border-radius: 50%; border: 2px solid #264b5d; object-fit: cover;' 
             src='https://imagizer.imageshack.com/img923/8858/imdiKf.jpg' 
             alt='fad admin logo' 
             width='60px' 
             height='60px'>
        <div style='font-family: "L ucida Handwriting", cursive; color: white;'>
        {title}      
        </div>
    </div>
    """
)

admin.site.site_title = _("Fad cargo Administartsiyasi")
admin.site.index_title = _("Fad cargo admin ga xush kelibsiz!")

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    prefix_default_language=True
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]
