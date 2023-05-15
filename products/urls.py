from django.urls import include, path
from .views import PartnerUpdate, ProductsViewSet

from rest_framework import routers
router = routers.SimpleRouter()


urlpatterns = [
    path('upload/', PartnerUpdate.as_view()),
    path('products', ProductsViewSet.as_view({'get': 'list'})),

]
