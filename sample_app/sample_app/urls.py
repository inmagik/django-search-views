from django.conf.urls import url
from django.contrib import admin
from actors.views import ActorsView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', ActorsView.as_view(), name="actors"),
]
