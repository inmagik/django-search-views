from django.conf.urls import url
from django.contrib import admin
from actors.views import ActorsView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', ActorsView.as_view(), name="actors"),
]

from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
