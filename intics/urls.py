from django.contrib import admin
from django.urls import path, include

context_path = 'copro/'

urlpatterns = [
    path(context_path + 'admin/', admin.site.urls),
    path(context_path + "api/", include("app.urls")),
]
