from django.conf.urls import re_path, include

app_name = "djangofile"

urlpatterns = [
    re_path(r"^api/", include("djangofile.rest_api.urls")),
]