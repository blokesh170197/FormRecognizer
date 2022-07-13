from django.urls import path, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from .views import InformationExtraction

schema_view = get_swagger_view(title='Pastebin API')

router = routers.DefaultRouter()
router.register(r'information-extraction', InformationExtraction, basename="information-extraction")

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls)),
]