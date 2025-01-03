from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.utils.safestring import mark_safe

from root import settings

admin.site.site_header = mark_safe(
    """
    <div style='display: flex; align-items: center; gap: 10px;'>
        <img style='border-radius: 50%; border: 2px solid #264b5d; object-fit: cover;' 
             src='https://imagizer.imageshack.com/img923/8858/imdiKf.jpg' 
             alt='fad admin logo' 
             width='60px' 
             height='60px'>
        <div style='font-family: "L ucida Handwriting", cursive; color: white;'>
            ❄️ Faad Cargo Administration ❄️
        </div>
    </div>
    """
)

admin.site.site_title = "Fad cargo Administration"
admin.site.index_title = "Welcome to Fad cargo admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
