from django.urls import path, include
from rest_framework import routers

from .views import InformationExtraction

router = routers.DefaultRouter()
router.register(r'information-extraction', InformationExtraction, basename="information-extraction")

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls)),
]